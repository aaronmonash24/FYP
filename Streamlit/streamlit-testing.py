import streamlit as st
import mysql.connector
import pandas as pd



connection = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = ''
)


st.title('my FIT3164 streamlit hehe')

print('connected')

# connect to mysql
cursor = connection.cursor()
cursor.execute("Select * from food2")
data = cursor.fetchall()
print(cursor.column_names)

df = pd.DataFrame(data,columns = cursor.column_names)

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
