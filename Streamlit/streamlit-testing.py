import streamlit as st
import mysql.connector
import pandas as pd
import statsmodels.api as sm 
import numpy as np

# connect mysql
connection = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'atsu0218',
    database = 'fyp'
)

cursor = connection.cursor()
cursor.execute("select * from new_table")
data = cursor.fetchall()

# create dataframe
st.title('my FIT3164 streamlit hehe')
df = pd.DataFrame(data,columns = cursor.column_names)
df['Price'] = df['Price'].astype('float')
df['Quantity'] = df['Quantity'].astype('int')

# calculate PED
def calculate_ped(group):
    X = sm.add_constant(group['Price'])
    model = sm.OLS(group['Quantity'], X).fit()
    price_coef = model.params['Price']
    # mean_sellprice = group['Price'].mean()
    # mean_quantity = group['Quantity'].mean()
    # ped = price_coef * (mean_sellprice / mean_quantity)
    group.loc[:, 'PED'] = price_coef # Assign the computed PED values to the 'PED' column
    return group

df = df.groupby('ID').apply(calculate_ped).reset_index(drop=True)


# search bar
text_search = st.text_input("Search by ID", value="")
m1 = df["ID"].str.contains(text_search)
df_search = df[m1]
if text_search:
    st.write(df_search)


# filter category via 
list = df.Category.unique()
selection = st.multiselect('Select list', list, ['Food','Hobbies','Households'])
df_selection = df[df.Category.isin(selection)]



# Display DataFrame
df_editor = st.dataframe(df_selection)