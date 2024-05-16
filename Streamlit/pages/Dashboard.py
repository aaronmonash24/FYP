import streamlit as st
from time import time
import numpy as np
import pandas as pd 
# import matplotlib as 
import plotly.express as px
from datetime import timedelta
st.set_page_config(page_title="Plotting Demo", page_icon="📈", layout = "wide")
t_start = time()
# """
# Dashboard Overview:

# This dashboard provides visual representations of data spanning the last 30 days. 
# The dashboard displays a key metric at the top of the page, providing a quick snapshot of the most critical data point for the last 30 days, which is total sales and total revenue.
# It also includes both bar graphs and line graphs to illustrate various metrics and trends over this period. 
# This is designed to give users an immediate understanding of a vital aspect of the dataset.

# Components:
# 1. Metrics: These metrics serve as a quick indicator of total sales and total revenue.
# 2. Bar Graphs: These are used to show discrete changes and comparisons across different categories or groups within the data collected over the past 30 days. 
# 3. Line Graphs: These graphs are employed to depict continuous data over time, allowing for the observation of trends and the impact of day-to-day changes. 

# Author: Chloe Ang, Edrick Hendri
# """

# Page configuration
st.markdown("# Dashboard")

# Work below is done by Chloe Ang
# Replace the datas inside with the data in local computer

st.session_state.cursor.execute("select * from 3month where date >= '2016-02-15'")
df= st.session_state.cursor.fetchall()
data=pd.DataFrame(df,columns = st.session_state.cursor.column_names)
data['date'] = pd.to_datetime(data['date'], errors='coerce')
# Find the latest date in the data
latest_date = data['date'].max()

# Calculate the date 28 days before the latest date
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

# Calculate total revenue and sales for last 28 days
total_revenue = filtered_data['revenue'].sum()  
total_sales = filtered_data['sold'].sum() 

# Calculate total revenue and sales for last 56 days
previous_total_revenue = previous_data['revenue'].sum()
previous_total_sales = previous_data['sold'].sum()

# Calculate the percentage change for revenue
delta_revenue = total_revenue - previous_total_revenue
delta_revenue_percentage = ((delta_revenue) / previous_total_revenue * 100) if previous_total_revenue != 0 else 0

# Calculate the percentage change for sales
delta_sales = total_sales - previous_total_sales
delta_sales_percentage = ((delta_sales) / previous_total_sales * 100) if previous_total_sales != 0 else 0

# Work below is done by Edrick Hendri
# Display metrics
# Getting the barchart
bar_df = filtered_data[["cat_id", "sold"]].groupby("cat_id", as_index= False).sum()

# Create the df for bar graph
line_df = filtered_data[["cat_id", "date", "revenue"]].groupby(["cat_id", "date"], as_index= False).sum()

# Create sales trend analysis
placeholder = st.empty()
with placeholder.container():
    col1, col2 =  st.columns([1,1])
    col1.metric(label="Total Revenue for the last 28 Days (in USD)" , value=f"${total_revenue:,.2f}",delta=f"{delta_revenue_percentage:.2f}%")
    col2.metric(label="Total Sales for the last 28 Days " , value=f"{total_sales:,} Units",delta=f"{delta_sales_percentage:.2f}%")

    fig_col1, fig_col2 = st.columns([1,1])
    with fig_col1:
        fig2=px.line(line_df,x='date',y='revenue', color='cat_id', labels={'date': 'Date', 'revenue':'Total Revenue'})
        st.plotly_chart(fig2, use_container_width=True)
        
    with fig_col2:
        fig=px.bar(bar_df,x='sold',y='cat_id', orientation='h', text_auto=True, labels={'sold': 'Quantity Sold', 'cat_id':'Category'},color = 'cat_id')
        # Adjusting figure layout properties to make it aligned
        fig.update_layout(
            autosize=True,
            margin=dict(l=20, r=20, t=20, b=150)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        
t_end = time()
print('Dashboard loading time took %.3f second' % (t_end - t_start))