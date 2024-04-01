import streamlit as st
import mysql.connector
import pandas as pd
import statsmodels.api as sm 
import numpy as np
from sqlalchemy import create_engine
from streamlit_modal import Modal
from time import  time

# connect mysql
connection = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'root',
    database = 'hobbies'
)

col1, col2, col3 = st.columns(3)
col1.metric("Profit", "70 M", "1.2% ")
col2.metric("Revenue", "210.9", "1.8%")
col3.metric("Sales", "31.2", "4%")
cursor = connection.cursor()
#cursor.execute("Select * from food2 ")
#data = cursor.fetchall()
#print(cursor.column_names)

def insert_chunks(df):
    df_iter = pd.read_csv(df, iterator=True, chunksize=100000)
    
    chunk=next(df_iter).dropna()
    engine = create_engine('mysql://root:root@localhost:3306/hobbies')

    
    for chunk in df_iter :
        t_start = time()

        chunk = chunk.dropna()

        
        chunk.to_sql(name='food2', con=engine, if_exists='append',schema='hobbies',index=False)

        t_end = time()

        print('inserted another chunk, took %.3f second' % (t_end - t_start))
t_start = time()
#insert_chunks("hobbies.csv")
t_end = time()
print('Total time took %.3f second' % (t_end - t_start))
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
    #ped = price_coef * (mean_sellprice / mean_quantity)
    ped=mean_quantity
    return ped







#df_2=df.groupby(['YearMonth','ID']).apply(calculate_ped).reset_index(drop=True)
#df_2=df.groupby(['ID','YearMonth'])


df_2=df.groupby(['ID','YearMonth'])
test = df_2.aggregate({'Quantity':np.sum,'Price':np.mean})
first_values = sorted(pd.DataFrame([t[0] for t in test.index])[0].unique())
final=[]
# a version of calculate_ped, using this as its slightly diff and I dont wanna change things too much
for i in range(len(first_values)):
    X = sm.add_constant(test.loc[first_values[i]]['Price'])
    model = sm.OLS(test.loc[first_values[i]]['Quantity'], X).fit()
    mean_sellprice = np.mean(test.loc[first_values[i]]['Price'])
    mean_quantity = np.mean(test.loc[first_values[i]]['Quantity'])
    ped = model.params['Price'] * (mean_sellprice / mean_quantity)
    final.append([first_values[i],ped])
final=pd.DataFrame(final,columns=["Product ID","Predicted PED"])
#df = df.groupby('ID').apply(calculate_ped).reset_index(drop=True)

"""

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
"""
df_editor=st.dataframe(df.head(100))
df_editor=st.dataframe(final)
#df_editor=st.dataframe(df_3)
print("Hello")

# display button
open_model = st.button("Open Chart")
modal = Modal(key = "Demo key",title = "Testing" )

# display button
modal_btn = st.button("Open Chart")
modal = Modal(key = "Demo key",title = "Testing" )

if modal_btn:
    modal.open()

if modal.is_open():
    with modal.container():
        st.title("Testing")








