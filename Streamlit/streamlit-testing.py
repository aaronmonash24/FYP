import streamlit as st
import mysql.connector
import pandas as pd
import statsmodels.api as sm 
import numpy as np
from time import time



connection = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'Keer2001!',
    database = 'new_schema'
    password = 'root',
    database = 'hobbies'
)


st.title('my FIT3164 streamlit hehe')

print('connected')

# connect to mysql
cursor = connection.cursor()
cursor.execute("Select * from food")
data = cursor.fetchall()
print(cursor.column_names)

df = pd.DataFrame(data,columns = cursor.column_names)
df['Price'] = df['Price'].astype('float')
df['Quantity'] = df['Quantity'].astype('int')

# calculate PED
def calculate_ped(group):
    X = sm.add_constant(group['Price'])
    model = sm.OLS(group['Quantity'], X).fit()
    price_coef = model.params['Price']
    print(model.params['Price'])
    # mean_sellprice = np.mean(group['Price'])
    # mean_quantity = np.mean(group['Quantity'])
    # ped = price_coef * (mean_sellprice / mean_quantity)
    group.loc[:, 'PED'] = price_coef
    return price_coef


import statsmodels.api as sm
import pandas as pd

def calculate_ped(group):
    X = sm.add_constant(group['Price'])
    model = sm.OLS(group['Quantity'], X).fit()
    price_coef = model.params['Price']
    # mean_sellprice = group['Price'].mean()
    # mean_quantity = group['Quantity'].mean()
    # ped = price_coef * (mean_sellprice / mean_quantity)
    group.loc[:, 'PED'] = price_coef # Assign the computed PED values to the 'PED' column
    return group

# Assuming df is your DataFrame
df = df.groupby('ID').apply(calculate_ped).reset_index(drop=True)


insert_chunks("hobbies_df.csv")
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

print("Hello")