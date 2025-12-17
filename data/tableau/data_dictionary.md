# Data Dictionary for Tableau Analysis

This document describes all columns in the combined datasets.

## 10-Year Break-Even Analysis

**File:** `break_even_10yr_combined.csv`

| Column Name | Description |
|-------------|-------------|
| Date | Date of the month (YYYY-MM-DD) |
| Month | Month number (1-120) |
| City | City name (NYC, Utica, Buffalo) |
| Cumulative_Buying | Total cumulative costs for buying scenario ($) |
| Cumulative_Renting | Total cumulative costs for renting scenario ($) |
| Cost_Difference | Difference between buying and renting costs ($) |
| Buying_Monthly | Monthly cost for buying scenario ($) |
| Renting_Monthly | Monthly cost for renting scenario ($) |
| Is_BreakEven | Boolean indicating if break-even point reached |
| BreakEven_Month | Month number when break-even occurs (if applicable) |
| BreakEven_Date | Date when break-even occurs (if applicable) |

## 30-Year Break-Even Analysis

**File:** `break_even_30yr_combined.csv`

| Column Name | Description |
|-------------|-------------|
| Date | Date of the month (YYYY-MM-DD) |
| Month | Month number (1-360) |
| City | City name (NYC, Utica, Buffalo) |
| Cumulative_Buying | Total cumulative costs for buying scenario ($) |
| Cumulative_Renting | Total cumulative costs for renting scenario ($) |
| Cost_Difference | Difference between buying and renting costs ($) |
| Buying_Monthly | Monthly cost for buying scenario ($) |
| Renting_Monthly | Monthly cost for renting scenario ($) |
| Is_BreakEven | Boolean indicating if break-even point reached |
| BreakEven_Month | Month number when break-even occurs (if applicable) |
| BreakEven_Date | Date when break-even occurs (if applicable) |

## 10-Year Wealth Projection

**File:** `wealth_projection_10yr_combined.csv`

| Column Name | Description |
|-------------|-------------|
| Date | Date of the month (YYYY-MM-DD) |
| Month | Month number (1-120) |
| City | City name (NYC, Utica, Buffalo) |
| Buying_Wealth | Net wealth for buying scenario (Equity - Cumulative Costs) ($) |
| Renting_Wealth | Net wealth for renting scenario (Investment Value - Cumulative Rent) ($) |
| Wealth_Difference | Difference between buying and renting wealth ($) |
| Buying_Equity | Equity value for buying scenario ($) |
| Buying_CumulativeCosts | Total cumulative costs for buying scenario ($) |
| Renting_InvestmentValue | Investment value for renting scenario ($) |
| Renting_CumulativeRent | Total cumulative rent paid ($) |

## 10-Year Net Present Value Analysis

**File:** `npv_10yr_combined.csv`

| Column Name | Description |
|-------------|-------------|
| Date | Date of the month (YYYY-MM-DD) |
| Month | Month number (1-120) |
| City | City name (NYC, Utica, Buffalo) |
| Buying_Discounted_CF | Discounted cash flow for buying scenario ($) |
| Renting_Discounted_CF | Discounted cash flow for renting scenario ($) |
| Buying_Cumulative_NPV | Cumulative NPV for buying scenario ($) |
| Renting_Cumulative_NPV | Cumulative NPV for renting scenario ($) |
| Buying_Net_CF | Net cash flow for buying scenario (monthly, excludes final inflow) ($) |
| Renting_Net_CF | Net cash flow for renting scenario (monthly, excludes final inflow) ($) |

