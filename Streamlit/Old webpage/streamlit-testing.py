import streamlit as st
import mysql.connector
import pandas as pd
import statsmodels.api as sm 
import numpy as np
from sqlalchemy import create_engine
from streamlit_modal import Modal
from time import  time

# connect mysql

st.title('Retail Price Optimization')
col1, col2, col3 = st.columns(3)
col1.metric("Profit", "70 M", "1.2% ")
col2.metric("Revenue", "210.9", "1.8%")
col3.metric("Sales", "31.2", "4%")


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
t_start = time()
@st.cache_data
def fetch_data():
    
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
    df = pd.DataFrame(data,columns = cursor.column_names)
    return data,df

data,df=fetch_data()
t_end = time()
print('Fetching data total time took %.3f second' % (t_end - t_start))



# Discount slider
discount = st.slider('How much discount would you like to give', 0, 100, 10)




df['Price'] = df['Price'].astype('float')
df['Quantity'] = df['Quantity'].astype('int')



t_start = time()

@st.cache_data
def group_df(df):
    temp=df.groupby(['ID','YearMonth','Category','State_ID'])

    return temp
df_2=group_df(df)

t_end = time()
print('Group data total time took %.3f second' % (t_end - t_start))


test = df_2.aggregate({'Quantity':np.sum,'Price':np.mean})
first_values = sorted(pd.DataFrame([t[0] for t in test.index])[0].unique())
@st.cache_data
def calc_ped(grouped,values):
    final=[]
    for i in range(len(values)):
        X = sm.add_constant(grouped.loc[values[i]]['Price'])
        model = sm.OLS(grouped.loc[values[i]]['Quantity'], X).fit()
        mean_sellprice = np.mean(grouped.loc[values[i]]['Price'])
        mean_quantity = np.mean(grouped.loc[values[i]]['Quantity'])
        ped = model.params['Price'] * (mean_sellprice / mean_quantity)
        last_quantity=grouped.loc[values[i]]['Quantity'].iloc[-1]
        last_price=grouped.loc[values[i]]['Price'].iloc[-1]
        new_quantity=last_quantity*(1+ped*(last_price*0.9-last_price)/last_price)
        cat=grouped.loc[values[i]].index[0][1]
        state=grouped.loc[values[i]].index[0][2]
        final.append([values[i],cat,state,ped,abs(new_quantity)])
    final=pd.DataFrame(final,columns=["Product ID","Category","State ID","Predicted PED","Predicted Quantity"])
    return final

final=calc_ped(test,first_values)
t_end = time()
print('Predict data total time took %.3f second' % (t_end - t_start))


#adding sales quantity to final data frame
#adding sales quantity to final data frame
q=[]
for i in range(len(first_values)):
    q.append(test.loc[final['Product ID'][i]]['Quantity'].to_list())
final[ 'Sales Chart'] = q

text_search = st.text_input("Search by ID", value="")
m1 = df["ID"].str.contains(text_search)
df_search = df[m1]
if text_search:
    st.write(df_search)

# filter category via 
categories_list = ['Food', 'Household', 'Hobbies']  # Explicitly define the list of categories

# Provide default values for multiselect
default_values = categories_list  # Set default values to all available categories

# Multiselect with adjusted default values
selection = st.multiselect('Select Cetegory', categories_list, default_values)

# Filter DataFrame based on selection
df_selection = final[final['Category'].isin(selection)]


# filter category via 
state_list = ['CA_1', 'CA_2', 'CA_3', 'TX_1', 'TX_2', 'WI_1', 'WI_2']  # Explicitly define the list of categories

# Provide default values for multiselect
default_values = state_list  # Set default values to all available categories

# Multiselect with adjusted default values
selection = st.multiselect('Select State ID', state_list, default_values)

# Filter DataFrame based on selection
df_selection = final[final['State ID'].isin(selection)]



df_editor=st.dataframe(final,column_config={"Sales Chart" :st.column_config.LineChartColumn(
            "Sales Chart (Last 30 Days)", y_min=0, y_max=50
        )})






# filter category via 
#list = df.Category.unique()
#selection = st.multiselect('Select list', list, ['Food','Hobbies','Households'])
#df_selection = df[df.Category.isin(selection)]















