import streamlit as st
import mysql.connector
import pandas as pd
import statsmodels.api as sm 
import numpy as np
from sqlalchemy import create_engine
from time import  time

# connect mysql
connection = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'root',
    database = 'hobbies'
)

cursor = connection.cursor()
cursor.execute("Select * from food2 ")
data = cursor.fetchall()
print(cursor.column_names)

def insert_chunks(df):
    df_iter = pd.read_csv(df, iterator=True, chunksize=100000)
    
    chunk=next(df_iter).dropna()
    engine = create_engine('mysql://root:root@localhost:3306/hobbies')


    
    for chunk in df_iter :
        t_start = time()

        chunk = chunk.dropna()

        
        chunk.to_sql(name='hobby', con=engine, if_exists='append',schema='hobbies',index=False)

        t_end = time()

        print('inserted another chunk, took %.3f second' % (t_end - t_start))

#insert_chunks("hobbies_df.csv")
cursor.execute("Select * from food2 ")
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
    mean_sellprice = np.mean(group['Price'])
    mean_quantity = np.mean(group['Quantity'])
    ped = price_coef * (mean_sellprice / mean_quantity)
    return ped
df_2=df.groupby('ID').apply(calculate_ped).reset_index(drop=True)
#df = df.groupby('ID').apply(calculate_ped).reset_index(drop=True)


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
df_editor=st.dataframe(df_2)
print("Hello")

# display button
open_model = st.button("Open Chart")
modal = Modal(key = "Demo key",title = "Testing" )









