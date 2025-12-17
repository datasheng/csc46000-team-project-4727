import streamlit as st
import plotly.express as px
import os
import data_loader

# Set page config
st.set_page_config(page_title="Rent vs Buy Analysis", layout="wide")

# Title
st.title("Rent vs Buy Analysis Dashboard")
st.markdown("""
This dashboard compares the financial implications of renting vs. buying a home in three cities: **NYC**, **Buffalo**, and **Utica**.
Select a city from the sidebar to view detailed analysis.
""")

# Sidebar
st.sidebar.header("Configuration")
city = st.sidebar.selectbox("Select City", ["NYC", "Buffalo", "Utica"])

st.header(f"Analysis for {city}")

# Load Data
with st.spinner(f"Loading data for {city}..."):
    try:
        if city == "NYC":
            house_df, rental_df = data_loader.load_nyc_data()
        elif city == "Utica":
            house_df, rental_df = data_loader.load_utica_data()
        elif city == "Buffalo":
            house_df, rental_df = data_loader.load_buffalo_data()
    except Exception as e:
        st.error(f"Error loading data for {city}: {e}")
        st.stop()

# Historical Trends Section
st.subheader("Historical Trends")
st.markdown("Interactive charts showing the historical movement of median house prices and rental prices.")

col1, col2 = st.columns(2)

with col1:
    st.write("### Median House Price")
    if not house_df.empty:
        fig_house = px.line(house_df, x='Date', y='MedianPrice', 
                            title=f"{city} Median House Price Over Time",
                            labels={'MedianPrice': 'Price ($)', 'Date': 'Year'})
        st.plotly_chart(fig_house)
    else:
        st.warning("House price data not available.")

with col2:
    st.write("### Median Rental Price")
    if not rental_df.empty:
        fig_rent = px.line(rental_df, x='Date', y='RentalPrice', 
                           title=f"{city} Median Rental Price Over Time",
                           labels={'RentalPrice': 'Price ($)', 'Date': 'Year'})
        st.plotly_chart(fig_rent)
    else:
        st.warning("Rental price data not available.")

# Financial Analysis Section
st.markdown("---")
st.subheader("Financial Analysis (Rent vs Buy)")
st.markdown("Static analysis results derived from comprehensive financial modeling.")

images = data_loader.get_financial_images(city)

if images:
    # Break Even Analysis
    st.write("### Break Even Analysis")
    col3, col4 = st.columns(2)
    
    with col3:
        if "break_even_10yr" in images and os.path.exists(images["break_even_10yr"]):
            st.image(images["break_even_10yr"], caption="10-Year Break Even Analysis", width="stretch")
        else:
            st.info("10-Year Break Even plot not available.")
            
    with col4:
        if "break_even_30yr" in images and os.path.exists(images["break_even_30yr"]):
            st.image(images["break_even_30yr"], caption="30-Year Break Even Analysis", width="stretch")
        else:
            st.info("30-Year Break Even plot not available.")

    # Wealth Projection
    st.write("### Wealth Projection")
    if "wealth_projection" in images and os.path.exists(images["wealth_projection"]):
        st.image(images["wealth_projection"], caption="Wealth Projection Comparison (Rent vs Buy)", width="stretch")
    else:
        st.info("Wealth Projection plot not available.")
else:
    st.warning("Financial analysis images configuration not found.")
