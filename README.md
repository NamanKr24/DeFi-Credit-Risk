## **Aave V2 Wallet Credit Scoring**

### **Overview**

This repository implements a **robust, interpretable machine learning pipeline** to assign a **credit score (0-1000)** to each wallet interacting with the Aave V2 protocol, based solely on **historical transaction behavior**.

- **Higher scores** indicate responsible and reliable usage.
- **Lower scores** indicate risky, bot-like, or exploitative behaviour.

---

### **Table of Contents**

- [Objective](#objective)
- [Architecture](#architecture)
- [Features Engineered](#features-engineered)
- [Processing Flow](#processing-flow)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Outputs](#outputs)
- [Files Included](#files-included)
- [License](#license)

---

### **Objective**

Design and implement a **one-step script** that:

1. **Reads** raw user transaction data (JSON).  
2. **Engineers features** indicative of wallet behaviour.  
3. **Calculates credit scores** using a weighted linear scoring logic.  
4. **Outputs** scores in a structured csv file for downstream analysis.

---

### **Architecture**

- **Input:** user-transactions.json (raw transaction records)  
- **Processing:**
  - Load data into dataframe
  - Group transactions by wallet
  - Engineer behavioural features
  - Calculate weighted scores (0-1000)
- **Output:** wallet_scores.csv

---

### **Features Engineered**

| Feature                     | Description |
|------------------------------|-------------|
| total_txns                 | Total number of transactions by wallet |
| num_deposits               | Number of deposits |
| num_borrows                | Number of borrows |
| num_repays                 | Number of repayments |
| num_redeems                | Number of redeemunderlying actions |
| num_liquidations           | Number of liquidation calls |
| total_deposit_amt          | Total deposited amount |
| total_borrow_amt           | Total borrowed amount |
| avg_deposit_amt            | Average deposit amount |
| avg_borrow_amt             | Average borrow amount |
| repay_borrow_ratio         | Total repaid / total borrowed |
| active_days                | Number of unique active days |
| txn_per_day                | Transactions per active day |
| unique_assets              | Number of unique assets interacted with |
| borrow_deposit_ratio       | Total borrowed / total deposited |

---

### **Processing Flow**

```
user-transactions.json
        ↓
Load JSON → Pandas DataFrame
        ↓
Group by wallet
        ↓
Feature Engineering
        ↓
Weighted Linear Scoring
        ↓
wallet_scores.csv
```
---

### **Usage**

1. **Install dependencies**

```bash
pip install -r requirements.txt
```
2. **Run the scoring script**
```bash
python score_wallets.py --input user-transactions.json --output wallet_scores.csv
```

### **Dependencies**

- pandas

- numpy

See requirements.txt for details.

### **Outputs**

- Column	Description
- wallet	Wallet address
- score	Calculated credit score (0-1000)

### **Files Included**

- score_wallets.py – Main scoring script.

- analysis.md – Post-scoring behavioural analysis and insights.

- README.md – This documentation file.

- requirements.txt – Required Python packages.

### **License**

This repository is intended for educational and evaluative purposes. Contact the author for any production usage, extension, or integration queries.
