import streamlit as st
import time
import numpy as np
import pandas as pd 
# import matplotlib as 
import plotly.express as px

st.set_page_config(page_title="Plotting Demo", page_icon="📈")

st.markdown("# Dashboard")
st.sidebar.header("Dashboard")

# col1, col2 = st.columns([3])

col1, col2, col3, col4= st.columns([1,1,1,1.5])
col1.metric("Profit", "70 M", "1.2% ")
col2.metric("Revenue", "210.9", "1.8%")
col3.metric("Sales", "31.2", "4%")

# col4.bar_chart({"hobbies": 30, "Food": 50, "Leisure": 15},)
df = pd.DataFrame({"category": ["Food", "hobbies", "Household"], "total_sales": [50, 35, 20]})
fig=px.bar(df,x='total_sales',y='category', orientation='h')
fig.update
col4.write(fig)


# second row
col_21, col_22 = st.columns([1,1])
# sales trend analysis
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
col_21.line_chart(chart_data)
col_22.write(chart_data)

