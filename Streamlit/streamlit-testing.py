import streamlit as st
import mysql.connector
import pandas as pd
from time import time
from sqlalchemy import create_engine


connection = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'root',
    database = ''
)


st.title('my FIT3164 streamlit hehe')

print('connected')

# connect to mysql
cursor = connection.cursor()
cursor.execute("Select * from hobby")
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










