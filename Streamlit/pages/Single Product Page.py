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


st.set_page_config(layout="wide")
#Author: Yu Wen Liew 32882807
#This page is responsible to show the forecasted sales of a single product based on the PED obtained and the LGBM model used to forecast.
#The dropdown list shows the choice of product and discount rate is used to set the amount of discount given



discount = st.slider('How much discount would you like to give', -100, 100, 0) 


t_start = time()


@st.cache_data
def fetch_data(id):
    
    
    cursor = st.session_state.cursor
    cursor.execute("Select * from final where `Product ID`='"+id+"'")
    data = cursor.fetchall()
    print(cursor.column_names)
    df = pd.DataFrame(data,columns = cursor.column_names)
    return df

def get_id():
    cursor = st.session_state.cursor
    cursor.execute("Select distinct `Product ID` from final")
    data = cursor.fetchall()
    print(cursor.column_names)
    return pd.DataFrame(data,columns = cursor.column_names)


t_end = time()
print('Fetching data total time took %.3f second' % (t_end - t_start))


ids=get_id()

option = st.selectbox('Select Product',ids['Product ID'])


final=fetch_data(option)
final['Original Price'] = final['Original Price'].astype('float')
final['Original Quantity'] = final['Original Quantity'].astype('float')
final['Overall PED']=final['Overall PED'].astype('double')
final['Week 1 PED']=final['Week 1 PED'].astype('double')
final['Week 2 PED']=final['Week 2 PED'].astype('double')
final['Week 3 PED']=final['Week 3 PED'].astype('double')
final['Week 4 PED']=final['Week 4 PED'].astype('double')

t_start = time()


def group_df(df):
    temp=df.groupby(['id','YearMonth','cat_id','store_id'])

    return temp



t_end = time()
print('Group data total time took %.3f second' % (t_end - t_start))

t_start = time()
#test = group_df(data).aggregate({'sold':np.sum,'sell_price':np.mean})

#first_values = sorted(pd.DataFrame([t[0] for t in test.index])[0].unique())
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



final['Discounted Price']=final['Original Price']*(1-discount/100)
#final['Predicted Quantity']=final['Original Quantity']*(1+final['Overall PED']*(final['Discounted Price']-final['Original Price'])/final['Original Price'])
final['Predicted Week 1 Quantity']=final['Original Quantity']*(1+final['Week 1 PED']*(final['Discounted Price']-final['Original Price'])/final['Original Price'])
final['Predicted Week 2 Quantity']=final['Original Quantity']*(1+final['Week 2 PED']*(final['Discounted Price']-final['Original Price'])/final['Original Price'])
final['Predicted Week 3 Quantity']=final['Original Quantity']*(1+final['Week 3 PED']*(final['Discounted Price']-final['Original Price'])/final['Original Price'])
final['Predicted Week 4 Quantity']=final['Original Quantity']*(1+final['Week 4 PED']*(final['Discounted Price']-final['Original Price'])/final['Original Price'])
final['Original Revenue']=final['Original Quantity']*final['Original Price']
final['Predicted Week 1 Revenue']=final['Predicted Week 1 Quantity']*final['Discounted Price']

t_end = time()
print('Predict data total time took %.3f second' % (t_end - t_start))

st.dataframe(final)
#st.write(final.to_html(), unsafe_allow_html=True)
t_start = time()


t_end = time()
cursor = st.session_state.cursor
cursor.execute("Select * from 3month where id='"+option+"'")
data = cursor.fetchall()
print(cursor.column_names)
df = pd.DataFrame(data,columns = cursor.column_names)
avg_pred_1=[final['Predicted Week 1 Quantity'][0]/7]*7
avg_pred_2=[final['Predicted Week 2 Quantity'][0]/7]*7
avg_pred_3=[final['Predicted Week 3 Quantity'][0]/7]*7
avg_pred_4=[final['Predicted Week 4 Quantity'][0]/7]*7
avg_pred=avg_pred_1+avg_pred_2+avg_pred_3+avg_pred_4
df['date']=pd.to_datetime(df['date'])
last_date=df['date'].max()

new_dates=pd.date_range(start=last_date + pd.Timedelta(days=1), periods=28, freq='D')
print(avg_pred)

new={'date':new_dates,
     'sold':avg_pred}
df_new=pd.DataFrame(new)

fig = px.line(df[df["id"]==option][-90:], x="date", y="sold", title='Forecasted Sales')
fig.add_trace(go.Scatter(x=df_new['date'], y=df_new['sold'],
                    mode='markers', name='Forecasted'))

st.plotly_chart(fig, use_container_width=True)
