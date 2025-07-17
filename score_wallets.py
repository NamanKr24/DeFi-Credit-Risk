import argparse
import json
import pandas as pd
import numpy as np

def load_transactions(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    token_decimals = {
        'USDC': 6,
        'WMATIC': 18,
        'WETH': 18,
        'DAI': 18,
        'USDT': 6,
        # Add other tokens as required
    }

    # Flatten actionData fields and convert amounts within the loop
    for record in data:
        ad = record.get('actionData', {})
        asset = ad.get('assetSymbol', None)
        raw_amt = ad.get('amount', 0)

        if asset in token_decimals:
            record['amount'] = float(raw_amt) / (10 ** token_decimals[asset])
        else:
            record['amount'] = float(raw_amt)  # default no conversion if unknown

        record['asset'] = asset

    df = pd.DataFrame(data)

    # Rename userWallet to wallet for consistency
    df.rename(columns={
        'userWallet': 'wallet',
    }, inplace=True)

    return df

def engineer_features(df):
    # Ensure required columns exist
    required_columns = ['wallet', 'action', 'amount', 'asset', 'timestamp']
    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing columns in input data: {missing_cols}")

    # Convert timestamp to datetime if needed
    if not np.issubdtype(df['timestamp'].dtype, np.datetime64):
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce')

    grouped = df.groupby('wallet')

    features = pd.DataFrame()

    # Transaction counts
    features['total_txns'] = grouped.size()
    features['num_deposits'] = grouped.apply(lambda x: (x['action'] == 'deposit').sum())
    features['num_borrows'] = grouped.apply(lambda x: (x['action'] == 'borrow').sum())
    features['num_repays'] = grouped.apply(lambda x: (x['action'] == 'repay').sum())
    features['num_redeems'] = grouped.apply(lambda x: (x['action'] == 'redeemunderlying').sum())
    features['num_liquidations'] = grouped.apply(lambda x: (x['action'] == 'liquidationcall').sum())

    # Financial aggregates
    features['total_deposit_amt'] = grouped.apply(lambda x: x.loc[x['action']=='deposit', 'amount'].sum())
    features['total_borrow_amt'] = grouped.apply(lambda x: x.loc[x['action']=='borrow', 'amount'].sum())
    features['avg_deposit_amt'] = grouped.apply(lambda x: x.loc[x['action']=='deposit', 'amount'].mean())
    features['avg_borrow_amt'] = grouped.apply(lambda x: x.loc[x['action']=='borrow', 'amount'].mean())

    # Repayment behavior
    total_repaid = grouped.apply(lambda x: x.loc[x['action']=='repay', 'amount'].sum())
    features['repay_borrow_ratio'] = total_repaid / features['total_borrow_amt']
    features['repay_borrow_ratio'].replace([np.inf, -np.inf], 0, inplace=True)
    features['repay_borrow_ratio'].fillna(0, inplace=True)

    # Activity consistency
    features['active_days'] = grouped.apply(lambda x: x['timestamp'].dt.date.nunique())
    features['txn_per_day'] = features['total_txns'] / features['active_days']
    features['txn_per_day'].fillna(0, inplace=True)

    # Diversity
    features['unique_assets'] = grouped.apply(lambda x: x['asset'].nunique())

    # Ratios
    features['borrow_deposit_ratio'] = features['total_borrow_amt'] / features['total_deposit_amt']
    features['borrow_deposit_ratio'].replace([np.inf, -np.inf], 0, inplace=True)
    features['borrow_deposit_ratio'].fillna(0, inplace=True)

    features.reset_index(inplace=True)

    return features

def calculate_scores(features):
    # Normalise features between 0-1 (robust min-max scaling)
    def robust_minmax(series):
        min_val = series.min()
        max_val = series.max()
        if max_val - min_val == 0:
            return pd.Series(0.5, index=series.index)  # neutral if no variation
        return (series - min_val) / (max_val - min_val)

    # Apply robust minmax
    for col in ['total_txns', 'num_deposits', 'num_borrows', 'num_repays', 'num_redeems',
                'total_deposit_amt', 'total_borrow_amt', 'repay_borrow_ratio',
                'active_days', 'txn_per_day', 'unique_assets']:
        features[f'norm_{col}'] = robust_minmax(features[col])

    # Score calculation (weights can be tuned)
    features['score'] = (
    + 0.3 * features['norm_total_deposit_amt']
    + 0.25 * features['norm_repay_borrow_ratio']
    + 0.15 * features['norm_active_days']
    + 0.1 * features['norm_unique_assets']
    + 0.1 * features['norm_num_repays']
    - 0.05 * robust_minmax(features['num_liquidations'])
    - 0.05 * robust_minmax(features['borrow_deposit_ratio'])
    )

    # Scale to 0-1000, clip to boundaries
    features['score'] = (features['score'] * 1000).clip(0, 1000).round(2)

    return features[['wallet', 'score']]

def main():
    parser = argparse.ArgumentParser(description="Score Aave V2 wallets based on transaction behavior")
    parser.add_argument("--input", required=True, help="Path to user-transactions.json")
    parser.add_argument("--output", required=True, help="Path to output scored wallets csv")

    args = parser.parse_args()

    print("Loading data...")
    df = load_transactions(args.input)

    print("Engineering features...")
    features = engineer_features(df)

    print("Calculating scores...")
    scores = calculate_scores(features)

    print(f"Writing scores to {args.output}...")
    scores.to_csv(args.output, index=False)

    print("Done.")

if __name__ == "__main__":
    main()