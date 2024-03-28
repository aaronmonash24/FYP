import streamlit as st
import mysql.connector
import pandas as pd
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


def insert_chunks(df):
    df_iter = pd.read_csv(df, iterator=True, chunksize=1000)
    df = next(df_iter)
    %time df.to_sql(name='hobby', con=engine, if_exists='append')


    while True: 
    t_start = time()

    df = next(df_iter)

    
    df.to_sql(name='hobby', con=engine, if_exists='append')

    t_end = time()

    print('inserted another chunk, took %.3f second' % (t_end - t_start))