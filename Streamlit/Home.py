import streamlit as st
import time
import numpy as np
import mysql.connector
st.set_page_config(page_title="Home", page_icon="")
# """
# Home page.

# This home page will show the introduction of the group and the whole webapp.
# It will introduce each of the group member and each of the section this project will 
# discusses.

# Author: Edrick Hendri
# """



st.markdown("# Home")
st.sidebar.header("Home")
st.write(
    """This FIT3164 project was created by the following member: Yu Wen Liew(Aaron), 
    Ke Er Ang(Chloe), Atsu Mizugochi, and Edrick Hendri. """
)

st.write( """This project aims to find pricing elasticity on retail products so that retail company
    could find the best strategy to optimize their sales.
    """)

if 'connection' not in st.session_state:
    st.session_state.connection=mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'root',
    database = 'hobbies'
    )
if 'cursor' not in st.session_state:
    st.session_state.cursor=st.session_state.connection.cursor()


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

