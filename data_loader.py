import pandas as pd
import os

def load_nyc_data():
    """Loads pre-processed data for NYC."""
    base_path = "data/cleaned_nyc"
    house_prices = pd.read_csv(os.path.join(base_path, "house_price_long.csv"))
    rental_prices = pd.read_csv(os.path.join(base_path, "rental_long.csv"))
    
    # Ensure Date column is datetime
    house_prices['Date'] = pd.to_datetime(house_prices['Date'])
    rental_prices['Date'] = pd.to_datetime(rental_prices['Date'])
    
    return house_prices, rental_prices

def load_utica_data():
    """Loads pre-processed data for Utica."""
    base_path = "data/output_utica"
    house_prices = pd.read_csv(os.path.join(base_path, "utica_house_price_long.csv"))
    rental_prices = pd.read_csv(os.path.join(base_path, "utica_rental_long.csv"))
    
    # Ensure Date column is datetime
    house_prices['Date'] = pd.to_datetime(house_prices['Date'])
    rental_prices['Date'] = pd.to_datetime(rental_prices['Date'])
    
    return house_prices, rental_prices

def load_buffalo_data():
    """Processes raw data to extract Buffalo data."""
    # Paths to raw data
    house_path = "data/two_family/two_bedroom_home_values_zhvi.csv"
    rental_path = "data/two_family/multifamily_rental_values_zori.csv"
    
    # Load and filter House Prices
    df_house = pd.read_csv(house_path)
    buf_house = df_house[df_house['RegionName'] == 'Buffalo, NY'].copy()
    
    # Process House Prices (melt and clean)
    # Assuming columns from index 5 onwards are dates (RegionID, SizeRank, RegionName, RegionType, StateName are first 5)
    # Actually, let's verify column structure dynamically or assume standard Zillow format
    # Standard Zillow: RegionID, SizeRank, RegionName, RegionType, StateName, then dates
    
    id_vars = ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']
    date_cols = [c for c in buf_house.columns if c not in id_vars]
    
    buf_house_long = buf_house.melt(id_vars=id_vars, value_vars=date_cols, var_name='Date', value_name='MedianPrice')
    buf_house_long['Date'] = pd.to_datetime(buf_house_long['Date'])
    buf_house_long = buf_house_long.dropna(subset=['MedianPrice'])
    buf_house_long = buf_house_long.sort_values('Date')

    # Load and filter Rental Prices
    df_rental = pd.read_csv(rental_path)
    buf_rental = df_rental[df_rental['RegionName'] == 'Buffalo, NY'].copy()
    
    # Process Rental Prices
    date_cols_rent = [c for c in buf_rental.columns if c not in id_vars]
    buf_rental_long = buf_rental.melt(id_vars=id_vars, value_vars=date_cols_rent, var_name='Date', value_name='RentalPrice')
    buf_rental_long['Date'] = pd.to_datetime(buf_rental_long['Date'])
    buf_rental_long = buf_rental_long.dropna(subset=['RentalPrice'])
    buf_rental_long = buf_rental_long.sort_values('Date')
    
    return buf_house_long, buf_rental_long

def get_financial_images(city):
    """Returns paths to financial analysis images for a given city."""
    images = {}
    
    if city == 'NYC':
        base_path = "data/output_nyc"
        images = {
            "break_even_10yr": os.path.join(base_path, "break_even_10yr.png"),
            "break_even_30yr": os.path.join(base_path, "break_even_30yr.png"),
            "wealth_projection": os.path.join(base_path, "wealth_projection_comparison.png")
        }
    elif city == 'Utica':
        base_path = "data/output_utica"
        images = {
            "break_even_10yr": os.path.join(base_path, "utica_break_even_10yr.png"),
            "break_even_30yr": os.path.join(base_path, "utica_break_even_30yr.png"),
            "wealth_projection": os.path.join(base_path, "utica_wealth_projection_comparison.png")
        }
    elif city == 'Buffalo':
        base_path = "data/output_buf"
        images = {
            "break_even_10yr": os.path.join(base_path, "break_even_10yr.png"),
            "break_even_30yr": os.path.join(base_path, "break_even_30yr.png"),
            "wealth_projection": os.path.join(base_path, "wealth_projection_comparison.png")
        }
        
    return images
