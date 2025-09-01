# Data Science Assignment: Trader Behavior vs. Market Sentiment

This repository contains the submission for the Data Science assignment for the Web3 Trading Team.

---

### Project Overview

The objective of this project is to analyze the relationship between trader behavior on the Hyperliquid platform and the broader Bitcoin market sentiment (Fear vs. Greed).

The analysis involves processing historical trade data to derive daily metrics such as trading volume, profitability, and user activity. These metrics are then compared against the daily Fear & Greed Index to identify patterns and signals in trader behavior.

---

### Directory Structure

The repository is structured according to the assignment instructions:

 - Analysis.ipynb
 - outputs/
   - sentiment_behavior_summary.png
   - volume_over_time_with_sentiment.png
 - ds_report.pdf
 - Instructions_Data-Science.pdf
 - README.md


---

### How to Run the Analysis

1.  **Environment:** The analysis was performed in **Google Colab**.
2.  **Data:** Download the two required datasets from the links provided in the assignment instructions and place them inside the directory.
3.  **Execution:** Open `Analysis.ipynb` in Google Colab. Ensure the file paths at the beginning of the notebook point to the datasets in the same directory.
4.  **Run All:** Execute all cells in the notebook sequentially from top to bottom.
5.  **Outputs:** The script will automatically generate and save the analysis plots to the `outputs/` directory.

---

### Key Libraries Used

* **pandas:** For data manipulation and analysis.
* **matplotlib & seaborn:** For data visualization.
* **numpy:** For numerical operations.
