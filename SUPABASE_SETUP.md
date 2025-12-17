# Supabase Setup Guide for NYC Analysis Data

This guide will help you set up Supabase and upload your NYC analysis CSV files.

## Prerequisites

1. **Supabase Account**: Sign up at [supabase.com](https://supabase.com) (free tier is fine)
2. **Python Package**: Install the Supabase Python client
   ```bash
   pip install supabase
   ```

## Step 1: Create a Supabase Project

1. Go to [app.supabase.com](https://app.supabase.com)
2. Click "New Project"
3. Fill in:
   - **Name**: Your project name (e.g., "NYC Housing Analysis")
   - **Database Password**: Choose a strong password (save this!)
   - **Region**: Choose closest to you
4. Wait for project to be created (takes 1-2 minutes)

## Step 2: Get Your Supabase Credentials

1. In your Supabase project dashboard, go to **Settings** (gear icon)
2. Click on **API** in the left sidebar
3. You'll need two values:
   - **Project URL**: Copy the "Project URL" (looks like `https://xxxxx.supabase.co`)
   - **Service Role Key**: Copy the "service_role" key (⚠️ Keep this secret! It has full database access)

## Step 3: Add Credentials to .env File

Open your `.env` file in the project root and add:

```env
FRED_API_KEY=e65e2af9b1240b2beb63c98940723f64
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your_service_role_key_here
```

Replace:
- `https://your-project-id.supabase.co` with your actual Project URL
- `your_service_role_key_here` with your actual service_role key

## Step 4: Create Tables in Supabase

You have two options:

### Option A: Use the SQL File (Recommended)

1. Open `supabase_create_tables.sql` in this project
2. Copy all the SQL code
3. In Supabase dashboard, go to **SQL Editor**
4. Click **New Query**
5. Paste the SQL code
6. Click **Run** (or press Ctrl+Enter)
7. You should see "Success. No rows returned" for each CREATE TABLE statement

### Option B: Let the Notebook Generate SQL

1. Run the Supabase cell in `nyc_analysis.ipynb`
2. It will print SQL statements
3. Copy and run them in Supabase SQL Editor

## Step 5: Upload CSV Data

1. Open `notebooks/nyc_analysis.ipynb`
2. Navigate to the last cell (Supabase Connection and CSV Upload)
3. Run the cell
4. It will:
   - Connect to Supabase
   - Upload all 4 CSV files:
     - `nyc_break_even_analysis.csv` (120 rows)
     - `nyc_break_even_analysis_30yr.csv` (360 rows)
     - `nyc_npv_analysis.csv` (120 rows)
     - `nyc_wealth_projection_10yr.csv` (120 rows)

## Step 6: Verify Data Upload

1. In Supabase dashboard, go to **Table Editor**
2. You should see 4 tables:
   - `nyc_break_even_analysis`
   - `nyc_break_even_analysis_30yr`
   - `nyc_npv_analysis`
   - `nyc_wealth_projection_10yr`
3. Click on each table to verify the data is there

## Troubleshooting

### Error: "relation does not exist"
- **Solution**: Make sure you ran the SQL to create tables first (Step 4)

### Error: "Invalid API key"
- **Solution**: Check that you're using the **service_role** key, not the anon key

### Error: "Connection refused"
- **Solution**: Check your SUPABASE_URL is correct and includes `https://`

### Tables exist but no data
- **Solution**: Check the cell output for error messages. You may need to run the upload cell again.

## Data Overview

### nyc_break_even_analysis (10-Year)
- **Rows**: 120 (10 years × 12 months)
- **Key Columns**: Date, Month, Cumulative_Buying, Cumulative_Renting, Cost_Difference
- **Purpose**: Compare buying vs renting costs over 10 years

### nyc_break_even_analysis_30yr (30-Year)
- **Rows**: 360 (30 years × 12 months)
- **Key Columns**: Same as 10-year, plus BreakEven_Month, BreakEven_Date
- **Purpose**: Long-term break-even analysis (break-even at Month 231)

### nyc_npv_analysis
- **Rows**: 120 (10 years)
- **Key Columns**: Buying/Renting Discounted CF, Cumulative NPV, Net CF
- **Purpose**: Net Present Value analysis with discounted cash flows

### nyc_wealth_projection_10yr
- **Rows**: 120 (10 years)
- **Key Columns**: Buying/Renting Wealth, Wealth_Difference, Equity, InvestmentValue
- **Purpose**: Wealth projection comparing equity growth vs investment returns

## Next Steps

Once data is uploaded, you can:
- Query the data using Supabase SQL Editor
- Build dashboards using Supabase's built-in tools
- Connect to other applications via Supabase API
- Set up Row Level Security (RLS) policies if needed

## Security Note

⚠️ **Important**: The service_role key has full database access. Never commit it to version control or share it publicly. Always use environment variables (`.env` file) and add `.env` to `.gitignore`.
