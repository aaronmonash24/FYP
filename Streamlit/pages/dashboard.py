import streamlit as st
import time
import numpy as np
import pandas as pd 
# import matplotlib as 
import plotly.express as px
from datetime import timedelta

# Page configuration
st.set_page_config(page_title="Plotting Demo", page_icon="📈", layout = "wide")
st.markdown("# Dashboard")
st.sidebar.header("Dashboard")

# replace the datas inside with the data in local computer
data = pd.read_csv("3month.csv")
data['date'] = pd.to_datetime(data['date'], errors='coerce')
# Find the latest date in the data
latest_date = data['date'].max()

# Calculate the date 30 days before the latest date
four_weeks_before_latest = latest_date - timedelta(days=28)
# Calculate previous period for the delta (changes)
start_of_previous_period = latest_date - timedelta(days=56)

# Filter data to the last 28 days from the latest date
filtered_data = data[(data['date'] <= latest_date) & (data['date'] > four_weeks_before_latest)].copy()

# Filter data to the last 56 days from the latest date
previous_data = data[(data['date'] > start_of_previous_period) & (data['date'] <= four_weeks_before_latest)].copy()

# Calculate the revenue for each row
filtered_data ['revenue'] = filtered_data ['sell_price'] * filtered_data ['sold']
previous_data ['revenue'] = previous_data ['sell_price'] * previous_data ['sold']

# Calculate total revenue and sales for last 30 days
total_revenue = filtered_data['revenue'].sum()  
total_sales = filtered_data['sold'].sum() 

# Calculate total revenue and sales for last 60 days
previous_total_revenue = previous_data['revenue'].sum()
previous_total_sales = previous_data['sold'].sum()

# Calculate the percentage change for revenue
delta_revenue = total_revenue - previous_total_revenue
delta_revenue_percentage = ((delta_revenue) / previous_total_revenue * 100) if previous_total_revenue != 0 else 0

# Calculate the percentage change for sales
delta_sales = total_sales - previous_total_sales
delta_sales_percentage = ((delta_sales) / previous_total_sales * 100) if previous_total_sales != 0 else 0


# Display metrics
# getting the barchart
bar_df = filtered_data[["cat_id", "sold"]].groupby("cat_id", as_index= False).sum()

# df for bar graph
line_df = filtered_data[["cat_id", "date", "revenue"]].groupby(["cat_id", "date"], as_index= False).sum()

# sales trend analysis

placeholder = st.empty()
with placeholder.container():
    col1, col2 =  st.columns([1,1])
    col1.metric(label="Total Revenue for 30 Days Ending " , value=f"{total_revenue:,.2f}",delta=f"{delta_revenue_percentage:.2f}%")
    col2.metric(label="Total Sales for 30 Days Ending " , value=f"{total_sales:,}",delta=f"{delta_sales_percentage:.2f}%")

    fig_col1, fig_col2 = st.columns([1,1])
    with fig_col1:
        st.caption("Revenue Made over the last 28 days:")
        fig2=px.line(line_df,x='date',y='revenue', color='cat_id', labels={'date': 'Date', 'revenue':'Total Revenue'})
        st.plotly_chart(fig2, use_container_width=True)
        
    with fig_col2:
        st.caption("quantity sold over the last 28 days:")
        fig=px.bar(bar_df,x='sold',y='cat_id', orientation='h', text_auto=True, labels={'sold': 'Quantity Sold', 'cat_id':'Category'})
        # Adjusting figure layout properties to make it aligned
        fig.update_layout(
            autosize=True,
            margin=dict(l=20, r=20, t=20, b=150)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        