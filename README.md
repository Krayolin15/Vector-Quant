# VectorQuant 🚀
**A High-Frequency Modular Backtesting Engine for Institutional Strategy Research.**

## 📌 Project Overview
VectorQuant is a professional-grade quantitative backtesting system designed to handle high-frequency (HF) market data. This engine was built with a focus on **speed**, **modularity**, and **mathematical accuracy**. 

Unlike standard loop-based backtesters, this framework utilizes **NumPy Vectorization** to process large datasets (tick or 5-second data) in milliseconds, allowing for rapid parameter optimization and strategy refinement.

## 🧠 Core Features
* **Vectorized Execution:** Uses Pandas/NumPy vectorization for O(1) time-complexity logic applications.
* **Modular Architecture:** Separation of the `Strategy Logic` from the `Execution Engine` and `Optimizer`.
* **Advanced Risk Metrics:** Calculations for Max Drawdown, Expectancy, Win Rate, and Net Profit.
* **Parameter Optimization:** Automated grid-search to identify 80%+ win rate configurations.
* **HFT Ready:** Built to handle sub-minute historical data formats (CSV/Parquet).

## 🛠️ Technical Stack
* **Language:** Python 3.x
* **Data Science:** Pandas, NumPy
* **Visualization:** Matplotlib
* **Environment:** Virtualenv / VPS Optimized

## 📂 Project Structure
* `quant_engine.py`: The core brain. Contains the simulation logic, math formulas, and data ingestion.
* `run_optimizer.py`: The researcher’s interface. Runs multi-parameter simulations to find the "Alpha."
* `data/`: (Excluded) Placeholder for high-frequency historical tick data.

## 📈 Performance Metrics Included
The system outputs a structured report for every run:
1.  **Win Rate (%):** Percentage of profitable trades.
2.  **Max Drawdown (%):** The peak-to-trough decline, measuring risk.
3.  **Expectancy:** The average amount you can expect to win (or lose) per trade, adjusted for probability.
4.  **Net Profit:** Total growth of capital after transaction fees.

## 🚀 Quick Start
Install dependencies:
Bash

pip install pandas numpy matplotlib
Run the Optimizer:

Bash

python run_optimizer.py
📝 Future Roadmap
[ ] Integration with Interactive Brokers (TWS) API for live execution.

[ ] Monte Carlo Simulation for stress-testing strategies.

[ ] Machine Learning (Scikit-Learn) implementation for signal filtering.

Developer: [Krayolin Kisten]
