import streamlit as st
import mysql.connector
import pandas as pd
import statsmodels.api as sm 
import numpy as np
from sqlalchemy import create_engine
from streamlit_modal import Modal
from time import  time
import plotly.express as px
from pathlib import Path
import plotly.graph_objects as go

import lightgbm as lgb
import mlforecast
from mlforecast import MLForecast
from mlforecast.lag_transforms import ExpandingMean, RollingMean, SeasonalRollingMean

"""
Author: Yu Wen Liew 32882807
This page is responsible to show the forecasted sales of a single product based on the PED obtained and the LGBM model used to forecast.
The dropdown list shows the choice of product and discount rate is used to set the amount of discount given
"""
def insert_chunks(df):
    df_iter = pd.read_csv(df, iterator=True, chunksize=10000)
    
    chunk=next(df_iter)
    engine = create_engine('mysql://root:root@localhost:3306/hobbies')

    for chunk in df_iter :
        t_start = time()

        chunk = chunk

        
        chunk.to_sql(name='food2', con=engine, if_exists='append',schema='hobbies',index=False)

        t_end = time()

        print('inserted another chunk, took %.3f second' % (t_end - t_start))

#insert_chunks("hobby.csv")
discount = st.slider('How much discount would you like to give', 0, 100, 10) 


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
    cursor.execute("Select * from hobby ")
    data = cursor.fetchall()
    print(cursor.column_names)
    df = pd.DataFrame(data,columns = cursor.column_names)
    return df



if 'data' not in st.session_state:
    st.session_state.data=fetch_data()
t_end = time()
print('Fetching data total time took %.3f second' % (t_end - t_start))

print(sum(st.session_state.data.memory_usage()))


st.session_state.data['sell_price'] = st.session_state.data['sell_price'].astype('float')
st.session_state.data['sold'] = st.session_state.data['sold'].astype('int')


t_start = time()


def group_df(df):
    temp=df.groupby(['id','YearMonth','cat_id','store_id'])

    return temp



t_end = time()
print('Group data total time took %.3f second' % (t_end - t_start))

t_start = time()
test = group_df(st.session_state.data).aggregate({'sold':np.sum,'sell_price':np.mean})
first_values = sorted(pd.DataFrame([t[0] for t in test.index])[0].unique())
t_end = time()
print('Aggregate data total time took %.3f second' % (t_end - t_start))


t_start = time()

def ped1(group):
    X = sm.add_constant(group['sell_price'])
    model = sm.OLS(group['sold'], X).fit()
    price_coef = model.params['sell_price']
    mean_sellprice = np.mean(group['sell_price'])
    mean_quantity = np.mean(group['sold'])
    ped = price_coef * (mean_sellprice / mean_quantity)

    return ped
hobby_ped=st.session_state.data.groupby(['cat_id']).apply(ped1)[0]

# a version of calculate_ped, using this as its slightly diff and I dont wanna change things too much
@st.cache_data
def calc_ped(grouped,values,disc,overall_ped):
    final=[]
    for i in range(len(values)):
        X = sm.add_constant(grouped.loc[values[i]]['sell_price'])
        model = sm.OLS(grouped.loc[values[i]]['sold'], X).fit()
        mean_sellprice = np.mean(grouped.loc[values[i]]['sell_price'])
        mean_quantity = np.mean(grouped.loc[values[i]]['sold'])
        ped = model.params['sell_price'] * (mean_sellprice / mean_quantity)
        if ped>0:
            ped=overall_ped
        last_quantity=grouped.loc[values[i]]['sold'].iloc[-1]
        last_price=grouped.loc[values[i]]['sell_price'].iloc[-1]
        new_quantity=last_quantity*(1+ped*(last_price*((100-disc)/100)-last_price)/last_price)
        cat=grouped.loc[values[i]].index[0][1]
        state=grouped.loc[values[i]].index[0][2]
        
        final.append([values[i],cat,state,ped,new_quantity])
    final=pd.DataFrame(final,columns=["Product ID","Category","State ID","Predicted PED","Predicted Quantity"])
    return final



st.session_state.final=calc_ped(test,first_values,discount,hobby_ped)




t_end = time()
print('Predict data total time took %.3f second' % (t_end - t_start))


t_start = time()

q=[]
for i in range(len(first_values)):
    q.append(test.loc[st.session_state.final['Product ID'][i]]['sold'].to_list())
st.session_state.final[ 'Sales Chart'] = q

option = st.selectbox('Select Product',st.session_state.final['Product ID'])

df_editor=st.dataframe(st.session_state.final[st.session_state.final["Product ID"]==option],column_config={"Sales Chart" :st.column_config.LineChartColumn(
            "Monthly Sales Chart", y_min=0, y_max=50
        )})


t_end = time()
avg_pred=st.session_state.final[st.session_state.final["Product ID"]==option]['Predicted Quantity'].to_list()[0]/28
st.session_state.data['date']=pd.to_datetime(st.session_state.data['date'])
last_date=st.session_state.data['date'].max()
print(last_date)
new_dates=pd.date_range(start=last_date + pd.Timedelta(days=1), periods=28, freq='D')
print(new_dates)
new={'date':new_dates,
     'sold':avg_pred}
df_new=pd.DataFrame(new)

fig = px.line(st.session_state.data[st.session_state.data["id"]==option][-90:], x="date", y="sold", title='Forecasted Sales')
fig.add_trace(go.Scatter(x=df_new['date'], y=df_new['sold'],
                    mode='markers', name='Forecasted'))

st.plotly_chart(fig, use_container_width=True)
print('The rest total time took %.3f second' % (t_end - t_start))