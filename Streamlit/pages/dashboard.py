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

data = pd.read_csv("/Users/chloeang/Desktop/FYP/FYP/Streamlit/3month.csv")
data['date'] = pd.to_datetime(data['date'], errors='coerce')
# Find the latest date in the data
latest_date = data['date'].max()

# Calculate the date 30 days before the latest date
thirty_days_before_latest = latest_date - timedelta(days=30)
# Calculate previous period for the delta (changes)
start_of_previous_period = latest_date - timedelta(days=60)

# Filter data to the last 30 days from the latest date
filtered_data = data[(data['date'] <= latest_date) & (data['date'] >= thirty_days_before_latest)]

# Filter data to the last 60 days from the latest date
previous_data = data[(data['date'] > start_of_previous_period) & (data['date'] <= thirty_days_before_latest)]

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
# st.metric(label="Total Revenue for 30 Days Ending " , value=f"{total_revenue:,.2f}",delta=f"{delta_revenue_percentage:.2f}%")
# st.metric(label="Total Sales for 30 Days Ending " , value=f"{total_sales:,}",delta=f"{delta_sales_percentage:.2f}%")


# col4.bar_chart({"hobbies": 30, "Food": 50, "Leisure": 15},)
df = pd.DataFrame({"category": ["Food", "hobbies", "Household"], "total_sales": [50, 35, 20]})
# fig=px.bar(df,x='total_sales',y='category', orientation='h')
# st.write(fig)


# sales trend analysis
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

placeholder = st.empty()
with placeholder.container():
    col1, col2 =  st.columns([1,1])
    col1.metric(label="Total Revenue for 30 Days Ending " , value=f"{total_revenue:,.2f}",delta=f"{delta_revenue_percentage:.2f}%")
    col2.metric(label="Total Sales for 30 Days Ending " , value=f"{total_sales:,}",delta=f"{delta_sales_percentage:.2f}%")

    fig_col1, fig_col2 = st.columns(2)
    with fig_col1:
        fig_col1.line_chart(chart_data)
        
    with fig_col2:
        fig=px.bar(df,x='total_sales',y='category', orientation='h')
        # Adjusting figure layout properties to make it responsive
        fig.update_layout(
            autosize=True,
            margin=dict(l=20, r=20, t=20, b=150)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        

