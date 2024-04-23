
import streamlit as st
import time
import numpy as np
import pandas as pd 
# import matplotlib as 
import plotly.express as px
from datetime import timedelta, datetime


st.set_page_config(page_title="Plotting Demo", page_icon="📈", layout = "wide")

st.markdown("# Dashboard")
st.sidebar.header("Dashboard")

# col1, col2 = st.columns([3])
col1, col2= st.columns([1,1,1.5])
col1.metric("Revenue", "210.9", "1.8%")
col2.metric("Sales", "31.2", "4%")

# load the dataset into a dataframe
df = pd.read_csv("3month.csv")
df["date"] = df["date"].apply(lambda x: pd.to_datetime(x))

# get the searching range for the data
latest_date = df["date"].max()
search_date = latest_date - timedelta(days=28)

# second row
col_21, col_22 = st.columns([1,1])

# sales trend analysis
print(df.head())
print(df.info())
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
# col_21.line_chart(chart_data)
# col_22.write(chart_data)

placeholder = st.empty()
with placeholder.container():
    fig_col1, fig_col2 = st.columns(2)
    with fig_col1:
        fig_col1.line_chart(chart_data)
        
    with fig_col2:
        pass
        # fig=px.bar(df,x='total_sales',y='category', orientation='h')
        # # Adjusting figure layout properties to make it responsive
        # fig.update_layout(
        #     autosize=True,
        #     margin=dict(l=20, r=20, t=20, b=150)
        # )
        # st.plotly_chart(fig, use_container_width=True)
        
        
