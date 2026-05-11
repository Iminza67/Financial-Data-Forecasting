# 📊 Financial Data Forecasting Dashboard

An interactive **S&P 500 quantitative analytics dashboard** designed to help quantitative analysts rapidly evaluate **risk-adjusted returns, volatility behavior, and cross-asset correlations** across equities.

The project integrates time-series market data with company fundamentals to support **data-driven equity screening and portfolio diagnostics**.

---

## 🎯 Research Question

How can quantitative analysts efficiently identify S&P 500 stocks and sectors that offer superior risk-adjusted returns, and what volatility and correlation dynamics explain these performance profiles?

---

## 🧠 Key Objective

To build a **dashboard-first analytical tool** that enables:

- Rapid equity screening across sectors  
- Identification of high Sharpe ratio stocks  
- Exploration of volatility regimes over time  
- Detection of correlation clusters for portfolio risk insights  

---

## 📂 Datasets

The project combines two open-source datasets:

- 📈 **S&P 500 Stocks Dataset**  
  https://www.kaggle.com/datasets/andrewmvd/sp-500-stocks  
  → Historical daily OHLCV market data  

- 🏢 **S&P 500 Companies with Financial Information**  
  https://www.kaggle.com/datasets/paytonfisher/sp-500-companies-with-financial-information  
  → Sector classification and fundamental financial indicators  

### 🔗 Data Integration Strategy
Both datasets are merged using the **Symbol (ticker)** field to combine:

- Time-series market behavior  
- Static company fundamentals  

---

## 👥 Stage Cast (Target Users)

- **Aria Chen & Marcus Webb**  
- Junior Quant Analysts at a ~$2B long/short equity hedge fund  

### Operational Context:
- Pre-market and intraday decision-making  
- High time pressure environment  
- Desktop-based analytical workflows  
- Preference for dense, information-rich visualizations  

### Core Tasks:
- Screening equities across sectors  
- Comparing risk-return profiles  
- Investigating volatility regimes  
- Validating portfolio correlation structures  

---

## 📊 Core Data Features

The final merged dataset supports multi-dimensional financial analysis using:

- **Symbol** → Stock identifier / join key  
- **Date** → Time-series index for analysis  
- **Close Price** → Return and Sharpe ratio calculations  
- **Volume** → Liquidity and confirmation signal  
- **Sector** → Grouping and comparative analysis  
- **Market Capitalization** → Size encoding in scatter plots  
- **Company Name** → Interactive tooltips / details-on-demand  

---

## 📈 Dashboard Components

### 1. Risk vs Return Analysis
- Scatter plot of Sharpe ratio vs volatility  
- Bubble size = market capitalization  
- Sector-based color encoding  

### 2. Candlestick Chart
- Stock-level OHLC visualization  
- Used for price structure and trend inspection  

### 3. Rolling Volatility Analysis
- Time-varying risk dynamics  
- Identification of volatility regimes  

### 4. Return Distribution Analysis
- Histogram of returns  
- Normal distribution overlay  

### 5. Correlation Heatmap
- Cross-asset correlation structure  
- Identification of sector clustering effects  

### 6. Volume Analysis
- Trading volume vs price movement validation  
- Liquidity behavior analysis  

---

## ⚙️ Technology Stack

- Python  
- Dash (Plotly)  
- Pandas  
- Plotly Express / Graph Objects  

---

## 🚀 Key Insights Enabled

This dashboard enables quantitative analysts to:

- Identify high Sharpe ratio stocks across sectors  
- Detect risk concentration in correlated assets  
- Compare valuation vs performance behavior  
- Monitor volatility shifts over time  
- Validate liquidity during price movements  

---

## 📌 Project Type

- Quantitative Finance Analytics  
- Interactive Data Visualization  
- Multi-source Financial Data Integration  
- Dashboard Engineering (Python Dash)  

---


## 📦 How to Run Locally

```bash
pip install -r requirements.txt
python app.py