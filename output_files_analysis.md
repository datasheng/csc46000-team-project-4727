# Output Files Analysis for Utica Analysis

## Current Files in `data/output_utica/` (19 files)

### ✅ ESSENTIAL FILES (Final Analysis Results - 9 files)

**Financial Analysis Results:**
1. `utica_break_even_analysis.csv` - 10-year break-even data
2. `utica_break_even_analysis_30yr.csv` - 30-year break-even data ⚠️ (currently named `utica_utica_break_even_analysis_30yr.csv`)
3. `utica_npv_analysis.csv` - NPV comparison
4. `utica_wealth_projection_10yr.csv` - Wealth projection

**Visualizations:**
5. `utica_break_even_10yr.png` - 10-year break-even chart ⚠️ (currently named `utica_utica_break_even_10yr.png`)
6. `utica_break_even_30yr.png` - 30-year break-even chart ⚠️ (currently named `utica_utica_break_even_30yr.png`)
7. `utica_combined_comparison.png` - Combined 10yr vs 30yr comparison ⚠️ (currently named `utica_utica_combined_comparison.png`)
8. `utica_wealth_projection_comparison.png` - Wealth projection comparison ⚠️ (currently named `utica_utica_wealth_projection_comparison.png`)

**Forecasts (Used in Analysis):**
9. `utica_arima_house_forecast.csv` - ARIMA house price forecasts
10. `utica_arima_rental_forecast.csv` - ARIMA rental price forecasts
11. `utica_arima_mortgage_forecast.csv` - ARIMA mortgage rate forecasts

### 📊 OPTIONAL BUT USEFUL (2 files)

12. `utica_arima_vs_prophet_comparison.png` - Model comparison visualization (useful for understanding why ARIMA was chosen)

### ❌ NOT NEEDED (Can be removed - 7 files)

**Prophet Forecasts (ARIMA was chosen, so these aren't used):**
- `utica_prophet_house_forecast.csv`
- `utica_prophet_rental_forecast.csv`
- `utica_prophet_mortgage_forecast.csv`
- `utica_prophet_forecasts.png`

**Intermediate Processed Data (unless needed for debugging):**
- `utica_house_price_long.csv` - Processed house price data
- `utica_rental_long.csv` - Processed rental data
- `utica_mortgage_monthly.csv` - Processed mortgage data
- `utica_merged_housing_data.csv` - Merged data

## Recommendations

1. **Fix naming issues**: Remove duplicate "utica_utica_" prefix from 5 files
2. **Keep essential files**: 9-11 files (financial results + visualizations + ARIMA forecasts)
3. **Optional**: Keep model comparison PNG (1 file)
4. **Remove**: Prophet forecast files (4 files) - not used since ARIMA was chosen
5. **Consider removing**: Intermediate data files (4 files) - only needed for debugging

**Total files after cleanup: 10-11 files** (down from 19)

