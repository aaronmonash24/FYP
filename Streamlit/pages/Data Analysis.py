"""  This Python script utilizes Streamlit to perform data analysis. 
The script loads HTML files containing data exploration and analysis results and Price Elasticity of Demand (PED) analysis. 
It embeds the HTML content in iframes to display it within the Streamlit application.
Author: Chloe Ang 
"""
import streamlit as st
import urllib.request
import ssl
st.set_page_config(layout="wide")
st.title("Data Analysis")
import streamlit.components.v1 as components

# Path to the HTML file
url = "https://raw.githubusercontent.com/Chloeangggg/FypDataAnalysis/main/DataExploration.html"
url2 = "https://raw.githubusercontent.com/Chloeangggg/FypDataAnalysis/main/PED.html"

# Load the HTML content
# with open(html_file_path, 'r') as f:
#     html_content = f.read()
context = ssl._create_unverified_context()
with urllib.request.urlopen(url, context=context) as response:
    html_content = response.read().decode()

# Embed the HTML content in an iframe
st.components.v1.html(html_content,width=800, height=600, scrolling=True)

st.title("Price Elasticity of Demand ")
with urllib.request.urlopen(url2, context=context) as response:
    html_content = response.read().decode()

# Embed the HTML content in an iframe
st.components.v1.html(html_content,width=800, height=600, scrolling=True)