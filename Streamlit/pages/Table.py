import streamlit as st
import mysql.connector
import pandas as pd
import statsmodels.api as sm 
import numpy as np
from time import  time


st.set_page_config(layout="wide")
st.markdown("# Product Table")

#In this page, we will allow users to explore the table by searching up the product by its ID,and filter product by category and store.
#Moreover, we can upload file(limited to csv) on the web application.
#
#Author: Atsu Mizoguchi 


st.session_state.cursor.execute("select * from final")
data = st.session_state.cursor.fetchall()

# create dataframe
df = pd.DataFrame(data,columns = st.session_state.cursor.column_names)


# search bar
text_search = st.text_input("Search by ID", value="")
m1 = df["Product ID"].str.contains(text_search)
df_search = df[m1]
if text_search:
    st.write(df_search)


# filter category via 
categories_list = ['FOODS', 'HOUSEHOLD', 'HOBBIES']  # Explicitly define the list of categories

# Provide default values for multiselect
default_values = categories_list  # Set default values to all available categories

# Multiselect with adjusted default values
selection = st.multiselect('Select category', categories_list, default_values)

# Filter DataFrame based on selection
df_selection = df[df['Category'].isin(selection)]

df_editor = st.dataframe(df_selection)

# filter category via 
state_list = ['CA_1', 'CA_2', 'CA_3','CA_4', 'TX_1', 'TX_2','TX_3', 'WI_1', 'WI_2','WI_3']  # Explicitly define the list of categories

# Provide default values for multiselect
default_values = state_list  # Set default values to all available categories

# Multiselect with adjusted default values
selection = st.multiselect('Select store', state_list, default_values)

# Filter DataFrame based on selection
df_selection = df[df['State ID'].isin(selection)]
df_editor = st.dataframe(df_selection)

# Display DataFrame

uploaded_file = st.file_uploader("Choose a CSV file", type='csv')
if uploaded_file is not None:
    try:
        t_start = time()
        # Read the file as a DataFrame
        dataframe = pd.read_csv(uploaded_file)
        # Display the DataFrame as a table
        st.write(dataframe)
        t_end = time()

        print('Upload data took %.3f second' % (t_end - t_start))

    except Exception as e:
        st.error(f"Error: {e}")





