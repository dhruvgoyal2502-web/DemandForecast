# Demand Forecasting using Statistical & Machine Learning Models

## Project Overview

This project focuses on building a comprehensive demand forecasting system using both classical statistical techniques and modern machine learning algorithms. The objective is to accurately predict future demand across multiple hierarchical levels, enabling data-driven decision-making in supply chain and inventory management.

---

## Key Features

* Implementation of diverse forecasting models (Statistical + ML)
* Hierarchical forecasting across product segments
* Automated forecasting pipeline using nested loops
* Robust data preprocessing for real-world noisy datasets
* Comparative model evaluation and performance analysis

---

## Models Implemented

### Statistical Models

* Moving Average
* Simple Exponential Smoothing (SES)
* Holt’s Linear Trend Model
* Holt-Winters Seasonal Model
* ARIMA / SARIMA

### Intermittent Demand Models

* Croston’s Method
* SBA (Syntetos–Boylan Approximation)

### Machine Learning Models

* Linear Regression
* Decision Tree Regressor
* Random Forest Regressor
* Gradient Boosting Regressor
* Extra Trees Regressor
* XGBoost Regressor

---

## Methodology

### 1. Data Preprocessing

* Cleaned and transformed raw demand data
* Converted non-numeric values and handled missing data
* Ensured time series consistency and ordering

### 2. Feature Engineering

* Created lag-based features for ML models
* Structured time-based inputs for forecasting

### 3. Model Development

* Built modular functions for each forecasting technique
* Ensured robustness for small, sparse, and irregular datasets

### 4. Hierarchical Forecasting

* Implemented nested loops to forecast across multiple levels
* Enabled scalable forecasting for different product categories

### 5. Model Evaluation

* Compared models using performance metrics (e.g., RMSE, MAPE)
* Identified best-performing models for different demand patterns

---

## Results & Insights

* Statistical models performed well for stable demand patterns
* Croston & SBA were effective for intermittent demand
* Tree-based models (Random Forest, XGBoost) captured complex patterns
* No single model fits all — performance varies by segment

---

## Tech Stack

* Python
* Pandas, NumPy
* Statsmodels
* Scikit-learn
* XGBoost
* Jupyter Notebook

---

## Conclusion

This project demonstrates a comprehensive approach to demand forecasting by combining statistical methods, machine learning models, and hierarchical forecasting techniques. It highlights the importance of selecting appropriate models based on demand patterns and building scalable solutions for real-world applications.

---
