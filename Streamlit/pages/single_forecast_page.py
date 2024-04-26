import streamlit as st
import mysql.connector
import pandas as pd
import statsmodels.api as sm 
import numpy as np
from sqlalchemy import create_engine
from streamlit_modal import Modal
from time import  time
import plotly.express as px

"""
Author: Yu Wen Liew 32882807
This page is responsible to show the forecasted sales of a single product based on the PED obtained and the LGBM model used to forecast.
The dropdown list shows the choice of product and discount rate is used to set the amount of discount given
"""
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

#insert_chunks("hobbies.csv")
discount = st.slider('How much discount would you like to give', 0, 100, 10) 


default="'HOBBIES_1_001_CA_1_validation'"
t_start = time()
connection = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'root',
    database = 'hobbies'
    )

@st.cache_data
def fetch_data():
    
    
    cursor = connection.cursor()
    cursor.execute("Select * from food2 ")
    data = cursor.fetchall()
    print(cursor.column_names)
    df = pd.DataFrame(data,columns = cursor.column_names)
    return df



if 'data' not in st.session_state:
    st.session_state.data=fetch_data()
t_end = time()
print('Fetching data total time took %.3f second' % (t_end - t_start))
print(discount)
st.session_state.data['Price'] = st.session_state.data['Price'].astype('float')
st.session_state.data['Quantity'] = st.session_state.data['Quantity'].astype('int')



t_start = time()


def group_df(df):
    temp=df.groupby(['ID','YearMonth','Category','State_ID'])

    return temp
df_2=group_df(st.session_state.data)

t_end = time()
print('Group data total time took %.3f second' % (t_end - t_start))

t_start = time()
test = df_2.aggregate({'Quantity':np.sum,'Price':np.mean})
first_values = sorted(pd.DataFrame([t[0] for t in test.index])[0].unique())
t_end = time()
print('Aggregate data total time took %.3f second' % (t_end - t_start))


t_start = time()

# a version of calculate_ped, using this as its slightly diff and I dont wanna change things too much
@st.cache_data
def calc_ped(grouped,values,disc):
    final=[]
    for i in range(len(values)):
        X = sm.add_constant(grouped.loc[values[i]]['Price'])
        model = sm.OLS(grouped.loc[values[i]]['Quantity'], X).fit()
        mean_sellprice = np.mean(grouped.loc[values[i]]['Price'])
        mean_quantity = np.mean(grouped.loc[values[i]]['Quantity'])
        ped = model.params['Price'] * (mean_sellprice / mean_quantity)
        last_quantity=grouped.loc[values[i]]['Quantity'].iloc[-1]
        last_price=grouped.loc[values[i]]['Price'].iloc[-1]
        new_quantity=last_quantity*(1+ped*(last_price*((100-disc)/100)-last_price)/last_price)
        cat=grouped.loc[values[i]].index[0][1]
        state=grouped.loc[values[i]].index[0][2]
        final.append([values[i],cat,state,-abs(ped),abs(new_quantity)])
    final=pd.DataFrame(final,columns=["Product ID","Category","State ID","Predicted PED","Predicted Quantity"])
    return final


if 'final' not in st.session_state:
    st.session_state.final=calc_ped(test,first_values,discount)


t_end = time()
print('Predict data total time took %.3f second' % (t_end - t_start))


t_start = time()

q=[]
for i in range(len(first_values)):
    q.append(test.loc[st.session_state.final['Product ID'][i]]['Quantity'].to_list())
st.session_state.final[ 'Sales Chart'] = q

option = st.selectbox('Select Product',st.session_state.final['Product ID'])

df_editor=st.dataframe(st.session_state.final[st.session_state.final["Product ID"]==option],column_config={"Sales Chart" :st.column_config.LineChartColumn(
            "Monthly Sales Chart", y_min=0, y_max=50
        )})

#text_search = st.text_input("Search by ID", value="")
#m1 = final["Product ID"].str.contains(text_search)
#df_search = final[m1]
#if text_search:
 #   st.dataframe(df_search,column_config={"Sales Chart" :st.column_config.LineChartColumn(
  #          "Sales Chart (Last 30 Days)", y_min=0, y_max=50
   #     )})

#df_editor=st.dataframe(df.head(100))
#df_editor=st.dataframe(final,column_config={"Sales Chart" :st.column_config.LineChartColumn(
  #          "Sales Chart (Last 30 Days)", y_min=0, y_max=50
  #      )})
#df_editor=st.dataframe(df_3)
t_end = time()

fig = px.line(st.session_state.data[st.session_state.data["ID"]==option][-90:], x="Date", y="Quantity", title='Life expectancy in Canada')
st.plotly_chart(fig, use_container_width=True)
print('The rest total time took %.3f second' % (t_end - t_start))