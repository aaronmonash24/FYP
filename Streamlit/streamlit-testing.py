import streamlit as st
import mysql.connector
import pandas as pd
import statsmodels.api as sm 
import numpy as np
from time import time



connection = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
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


# Assuming df is your DataFrame
df = df.groupby('ID').apply(calculate_ped).reset_index(drop=True)




# filter category via 
list = df.Category.unique()
selection = st.multiselect('Select list', list, ['Food','Hobbies','Households'])

df_selection = df[df.Category.isin(selection)]





# Display DataFrame
df_editor = st.dataframe(df_selection)

print("Hello")