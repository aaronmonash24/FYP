import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="Home", page_icon="")

st.markdown("# Home")
st.sidebar.header("Home")
st.write(
    """This FIT3164 Project was created by the following member: Yu Wen Liew(Aaron), 
    Ke er Ang(Chloe), Atsu mizugochi, and Edrick Hendri"""
)

st.write( """This Project aims to find Pricing elasticity on retail products so that retail company
    could find the best strategy to optimize their sales 
    """)

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)
chart = st.line_chart(last_rows)

for i in range(1, 101):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    status_text.text("%i%% Complete" % i)
    chart.add_rows(new_rows)
    progress_bar.progress(i)
    last_rows = new_rows
    time.sleep(0.05)

progress_bar.empty()

