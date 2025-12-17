
### Phase 3: Financial Modeling

#### Buying Scenario:
- **Initial Costs**: Down payment (20%) + closing costs (3%)
- **Monthly Costs**:
  - Mortgage payment (30-year fixed)
  - Property tax (0.88% annually)
  - Insurance (~$1,350/year)
  - Maintenance (1% of home value annually)
- **Equity Tracking**: Tracks loan balance and equity over time

#### Renting Scenario:
- **Monthly Costs**: Rent only
- **Opportunity Cost**: Invests $250,000 at 7% annual return (stock market)
- **Investment Growth**: Tracks investment value vs rent paid

### Phase 4: Break-Even Analysis

Compares cumulative costs of buying vs renting:
- **10 Years**: Renting is cheaper (no break-even)
- **30 Years**: Break-even at **month 231 (~19.2 years)**

### Phase 5: Advanced Metrics

- **NPV (Net Present Value)**: Present value of all cash flows
- **IRR (Internal Rate of Return)**: Return on buying investment
- **Wealth Projection**: Net wealth over time (equity/investment minus cumulative costs)

---

## Data Collection & Storage

### 1. Data Collection Mechanisms

#### A. House Prices (Zillow/ZHVI)
- **Source**: CSV files from Zillow Home Value Index (ZHVI)
- **Format**: Wide format with dates as columns
- **Collection Method**:
  ```python
  df = pd.read_csv('../data/two_family/two_bedroom_home_values_zhvi.csv')
  house_prices_df = df[df["RegionName"] == "New York, NY"].copy()
  ```
- **Processing Steps**:
  1. Filter for "New York, NY"
  2. Extract date columns (2015-01-31 onwards)
  3. Melt to long format: `Date | MedianPrice`
  4. Convert dates to datetime
  5. Forward fill missing values

#### B. Rental Prices (Zillow/ZORI)
- **Source**: CSV files from Zillow Observed Rent Index (ZORI)
- **Format**: Similar wide format
- **Collection Method**:
  ```python
  df_rental = pd.read_csv('../data/two_family/multifamily_rental_values_zori.csv')
  rental_prices_df = df_rental[df_rental['RegionName'] == 'New York, NY'].copy()
  ```
- **Processing Steps**:
  1. Filter for NYC
  2. Melt to long format
  3. Handle COVID gap (missing values) with time-based interpolation:
     ```python
     rental_long["RentalPrice"] = rental_long["RentalPrice"].interpolate(method="time")
     ```

#### C. Mortgage Rates (FRED API)
- **Source**: Federal Reserve Economic Data (FRED) API
- **API Details**:
  - Series: `MORTGAGE30US` (30-Year Fixed Rate Mortgage)
  - Frequency: Weekly data
  - Date range: 2015-01-01 to 2025-12-01
- **Collection Method**:
  ```python
  from fredapi import Fred
  fred = Fred(api_key=os.getenv("FRED_API_KEY"))
  mortgage = fred.get_series("MORTGAGE30US", 
                            start_date="2015-01-01", 
                            end_date="2025-12-01")
  ```
- **Processing Steps**:
  1. Convert to DataFrame
  2. Filter dates >= 2015-01-01
  3. Resample weekly → monthly (take mean):
     ```python
     mortgage_monthly = mortgage_df.resample("MS").mean()  # MS = Month Start
     ```

### 2. Data Storage Structure

#### Storage Hierarchy
```
data/
├── two_family/                    # Raw data (CSV files)
│   ├── two_bedroom_home_values_zhvi.csv
│   └── multifamily_rental_values_zori.csv
├── cleaned/                       # Processed/cleaned data
│   ├── house_price_long.csv       # Long format: Date, MedianPrice
│   ├── rental_long.csv            # Long format: Date, RentalPrice
│   ├── mortgage_monthly.csv       # Monthly: Date, mortgage_rate
│   └── merged_housing_data.csv   # FINAL MERGED DATASET
└── [analysis outputs]            # Generated analysis files
    ├── break_even_analysis.csv
    ├── break_even_analysis_30yr.csv
    ├── wealth_projection_10yr.csv
    └── npv_analysis.csv
```

#### Data Transformation Pipeline

**Step 1: Wide → Long Format**
- **Before (Wide)**:
  ```
  RegionName | 2015-01-31 | 2015-02-28 | 2015-03-31
  NYC        | 273827     | 274085     | 274448
  ```
- **After (Long)**:
  ```
  Date       | MedianPrice
  2015-01-31 | 273827
  2015-02-28 | 274085
  2015-03-31 | 274448
  ```
- **Code**:
  ```python
  price_long = price_data.melt(var_name="Date", value_name="MedianPrice")
  ```

**Step 2: Data Merging**
- Merge on Date column:
  ```python
  merged_df = pd.merge(price_long_reset, rental_long_reset, on='Date', how='inner')
  merged_df = pd.merge(merged_df, mortgage_reset, on='Date', how='inner')
  ```
- **Final Merged Structure**:
  ```
  Date       | MedianPrice | RentalPrice | mortgage_rate
  2015-01-01 | 273827      | 2264        | 3.67
  2015-02-01 | 274085      | 2278        | 3.71
  ```
- **Storage**:
  ```python
  merged_df.to_csv("../data/cleaned/merged_housing_data.csv", index=True)
  ```

---

## Forecasting Model Mechanics

### 1. Model Selection: ARIMA vs Prophet

The code uses both models, then selects **ARIMA**:
- **Prophet**: Facebook's time series model (handles seasonality automatically)
- **ARIMA**: Statistical model (more conservative, better for rates)

**Selection Logic**:
```python
FORECAST_METHOD = "ARIMA"  # Chosen because:
# - ARIMA provides more realistic mortgage rate forecasts
# - Prophet forecasted 14.61% (unrealistic) vs ARIMA 6.13% (reasonable)
```

### 2. ARIMA/SARIMA Model Training

#### Auto-ARIMA Parameter Search
```python
auto_model_house = auto_arima(
    house_prices_ts,           # Input time series
    start_p=0, start_q=0,      # Starting AR/MA orders
    max_p=5, max_q=5,          # Maximum AR/MA orders to test
    seasonal=True,              # Enable seasonal component
    m=12,                       # Seasonal period (12 months = yearly)
    stepwise=True,              # Stepwise search (faster)
    suppress_warnings=True,
    error_action='ignore',
    trace=True                  # Show search progress
)
```

**What This Does**:
- Tests different ARIMA(p,d,q) × (P,D,Q,s) combinations
- Finds optimal parameters using AIC (Akaike Information Criterion)
- Example result: `(2,1,2) × (1,1,1,12)` means:
  - AR(2), I(1), MA(2) for non-seasonal
  - Seasonal AR(1), I(1), MA(1) with 12-month period

#### Model Fitting
```python
arima_model_house = auto_model_house.fit(house_prices_ts)
```
- Trains on historical data (2015-2025)
- Learns patterns: trends, seasonality, autocorrelation

#### Forecast Generation
```python
forecast_periods = 120  # 10 years = 120 months
forecast_arima_house = arima_model_house.predict(
    n_periods=forecast_periods, 
    return_conf_int=True  # Get confidence intervals
)
```

**Output Structure**:
```python
forecast_arima_house_df = pd.DataFrame({
    'Date': forecast_dates,           # Future dates
    'forecast': forecast[0],          # Point forecast
    'lower': forecast[1][:, 0],       # Lower confidence bound
    'upper': forecast[1][:, 1]        # Upper confidence bound
}).set_index('Date')
```

### 3. Prophet Model (Alternative Method)

```python
# Prepare data (Prophet requires 'ds' and 'y' columns)
house_prices_prophet = price_long.rename(columns={'Date': 'ds', 'MedianPrice': 'y'})

# Create and fit model
model_house = Prophet()
model_house.fit(house_prices_prophet)

# Generate forecast
future_house = model_house.make_future_dataframe(periods=120, freq='M')
forecast_house = model_house.predict(future_house)
```

**Prophet Output Columns**:
- `yhat`: Forecast value
- `yhat_lower`: Lower confidence bound
- `yhat_upper`: Upper confidence bound
- `trend`: Trend component
- `seasonal`: Seasonal component

### 4. Forecast Storage and Usage

#### A. Forecast DataFrames (In-Memory)

After training, forecasts are stored as pandas DataFrames:
```python
# ARIMA forecasts
forecast_arima_house_df      # House prices forecast
forecast_arima_rental_df     # Rental prices forecast
forecast_arima_mortgage_df   # Mortgage rates forecast

# Structure:
# Index: Date (future dates)
# Columns: 'forecast', 'lower', 'upper'
```

#### B. Forecast Alignment

All three forecasts are aligned to a common date range:
```python
# Extract future forecasts (next 120 months)
house_prices_forecast = forecast_arima_house_df['forecast'].iloc[:120]
rental_prices_forecast = forecast_arima_rental_df['forecast'].iloc[:120]
mortgage_rates_forecast = forecast_arima_mortgage_df['forecast'].iloc[:120]

# Create aligned dataframe
forecasts_aligned = pd.DataFrame({
    'Date': forecast_dates,
    'HousePrice': house_prices_forecast.values,
    'RentalPrice': rental_prices_forecast.values,
    'MortgageRate': mortgage_rates_forecast.values
}).set_index('Date')
```

#### C. Forecast Usage in Financial Modeling

The aligned forecasts feed into the financial model:
```python
# For each month in 120-month analysis:
for month in range(120):
    house_price = forecasts_aligned['HousePrice'].iloc[month]
    rental_price = forecasts_aligned['RentalPrice'].iloc[month]
    mortgage_rate = forecasts_aligned['MortgageRate'].iloc[month]
    
    # Use these in calculations:
    # - Property tax (based on house_price)
    # - Maintenance (based on house_price)
    # - Rent payments (rental_price)
    # - Mortgage calculations (mortgage_rate)
```

#### D. Export to CSV (for Tableau/Analysis)

Forecasts are embedded in analysis outputs, not exported separately. The analysis results include forecasted values:

```python
# Break-even analysis (includes forecasted prices)
tableau_break_even.to_csv('../data/break_even_analysis.csv', index=False)

# Wealth projection (uses forecasted prices)
tableau_wealth.to_csv('../data/wealth_projection_10yr.csv', index=False)

# NPV analysis (uses forecasted prices)
npv_comparison.to_csv('../data/npv_analysis.csv', index=False)
```

---

## Key Findings

### 10-Year Analysis

**Renting is Cheaper**:
- Saves approximately **$60,000-$70,000** over 10 years
- **Buying Wealth**: -$156,000 (negative due to high upfront costs)
- **Renting Wealth**: +$24,000 (investment gains offset rent)

**Why Renting Wins Short-Term**:
1. Lower upfront costs (no down payment/closing costs)
2. Investment returns compound faster initially
3. More flexibility to move
4. No maintenance/property tax responsibilities

### 30-Year Analysis

**Break-Even Point**: Month 231 (19.2 years)
- **Before month 231**: Renting is cheaper
- **After month 231**: Buying becomes cheaper
- **Final Wealth Comparison**:
  - Buying: +$57,000
  - Renting: +$33,000
  - **Buying wins by ~$24,000** over 30 years

**Why Buying Wins Long-Term**:
1. **Mortgage Payoff**: After 30 years, no more mortgage payments
2. **House Appreciation**: Home value increases over time (243% over 30 years)
3. **Full Equity**: Own the asset outright
4. **Rent Increases**: Rent continues to rise (122% over 30 years)

### Key Insights

1. **Time Horizon Matters**: 
   - Short-term (0-19 years): Renting + Investing is more profitable
   - Long-term (19+ years): Buying becomes more profitable

2. **Break-Even at ~19 Years**: 
   - Buying becomes cheaper after this point
   - The advantage grows significantly after mortgage payoff (month 360)

3. **Mortgage Payoff is Key**: 
   - Buying advantage grows after the mortgage is paid off
   - No more mortgage payments = lower monthly costs

4. **Opportunity Cost**: 
   - Renting allows investing the down payment
   - 7% investment return helps short-term, but long-term house appreciation wins

5. **Market Assumptions**: 
   - Uses forecasted prices and rates
   - Results depend on these assumptions being accurate

---

## Technical Details

### Missing Data Handling

- **House Prices**: Forward fill (`fillna(method='ffill')`)
- **Rental Prices**: Time-based interpolation (`interpolate(method='time')`)
- **Mortgage Rates**: Resampling (weekly → monthly mean)

### Date Alignment

- All data converted to end-of-month timestamps
- Common date range: 2015-01-01 onwards
- Forecasts aligned to monthly frequency

### Model Parameters (ARIMA)

- **Search Space**: p, q ∈ [0, 5]
- **Seasonal**: m = 12 (monthly seasonality)
- **Optimization**: AIC (Akaike Information Criterion)
- **Method**: Stepwise search

### Forecast Extension (30-Year)

For 30-year analysis, forecasts are extended using trend:
```python
# Calculate growth rate from 120-month forecast
house_growth_rate = (forecast[-1] / forecast[0]) ** (1/120) - 1

# Extend using compound growth
for i in range(240):  # Additional 240 months
    last_value = last_value * (1 + house_growth_rate)
```

### Financial Assumptions

- **Budget**: $250,000 total
- **Down Payment**: 20% of house price
- **Closing Costs**: 3% of purchase price
- **Property Tax**: 0.88% annually (NYC rate)
- **Insurance**: $1,350/year
- **Maintenance**: 1% of home value annually
- **Opportunity Cost Rate**: 7% annual return (stock market)
- **Discount Rate**: 4% annual (for NPV calculations)

---

## Data Flow Diagram

```
┌─────────────────┐
│  RAW DATA       │
│  (CSV Files)    │
│  - House Prices │
│  - Rental Prices│
│  - Mortgage API │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  PREPROCESSING   │
│  - Filter NYC    │
│  - Wide→Long     │
│  - Handle NaN    │
│  - Interpolate   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  CLEANED DATA   │
│  (CSV Storage)  │
│  - house_price   │
│  - rental        │
│  - mortgage      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  MERGE DATA     │
│  (on Date)      │
│  - Inner join   │
│  - Align dates  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  TIME SERIES    │
│  PREPARATION    │
│  (Index by Date)│
│  - Set index    │
│  - Sort dates   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  MODEL TRAINING │
│  - ARIMA        │
│    * Auto-search│
│    * Fit model  │
│  - Prophet      │
│    * Fit model  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FORECASTS      │
│  (In-Memory)    │
│  - 120 months   │
│  - CI bounds    │
│  - 3 variables  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FORECAST       │
│  ALIGNMENT      │
│  (Common dates) │
│  - House Price  │
│  - Rental Price │
│  - Mortgage Rate│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FINANCIAL      │
│  MODELING       │
│  - Buying costs │
│  - Renting costs│
│  - Equity track │
│  - Investment   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ANALYSIS       │
│  - Break-even   │
│  - NPV/IRR      │
│  - Wealth proj. │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  OUTPUTS        │
│  (CSV Files)    │
│  - break_even    │
│  - wealth       │
│  - npv          │
└─────────────────┘
```

---

## Summary

### What This Project Does

1. **Collects** real estate data from multiple sources (Zillow, FRED API)
2. **Processes** and cleans the data for analysis
3. **Forecasts** future prices using time series models (ARIMA/SARIMA)
4. **Models** financial scenarios for buying vs renting
5. **Calculates** break-even points and wealth projections
6. **Exports** results for visualization and decision-making

### Key Technical Components

1. **Data Collection**: CSV files (Zillow) + API (FRED)
2. **Storage**: Hierarchical CSV structure (raw → cleaned → merged)
3. **Forecasting**: ARIMA/SARIMA with auto-parameter selection
4. **Forecast Storage**: In-memory DataFrames, embedded in analysis outputs

### Bottom Line for Decision-Making

- **Planning to stay <19 years?** → Renting is likely better financially
- **Planning to stay >19 years?** → Buying becomes more advantageous
- **The analysis quantifies** the trade-offs between flexibility (renting) and long-term wealth building (buying)

This model helps make an **informed decision** based on your time horizon and financial goals.

---

## Visualizations Generated

1. **Break-Even Charts**: Show when buying becomes cheaper
2. **Net Position Charts**: Compare financial outcomes over time
3. **Wealth Projection**: Shows wealth accumulation for both scenarios
4. **Cost Difference**: Visualizes the gap between buying and renting costs

All visualizations are saved as PNG files in the `data/` directory:
- `break_even_10yr.png`
- `break_even_30yr.png`
- `combined_comparison.png`
- `wealth_projection_comparison.png`

---

*Document generated for presentation purposes*
*Last updated: 2025*


