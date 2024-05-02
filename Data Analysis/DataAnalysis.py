"""  This Python script utilizes Streamlit to perform data analysis. 
The script loads HTML files containing data exploration and analysis results and Price Elasticity of Demand (PED) analysis. 
It embeds the HTML content in iframes to display it within the Streamlit application.
Author: Chloe Ang 
"""
import streamlit as st

st.title("Data Analysis")
import streamlit.components.v1 as components

# Path to the HTML file
html_file_path = "https://github.com/aaronmonash24/FYP/blob/main/Data%20Analysis/DataExploration.html"
html_file_path2 = "https://github.com/aaronmonash24/FYP/blob/main/Data%20Analysis/PED.html"
# Load the HTML content
with open(html_file_path, 'r') as f:
    html_content = f.read()

# Embed the HTML content in an iframe
st.components.v1.html(html_content,width=800, height=600, scrolling=True)

# Load the content of the second HTML file
with open(html_file_path2, 'r') as f:
    html_content2 = f.read()

# Embed the second HTML content in an iframe
st.title("PED Analysis")
components.html(html_content2, width=800, height=600, scrolling=True)