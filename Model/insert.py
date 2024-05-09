def insert_chunks(df):# to insert data into MySQL, provided table and CSV has same schema
    df_iter = pd.read_csv(df, iterator=True, chunksize=10000)
    
    #chunk=next(df_iter)
    engine = create_engine('mysql://root:root@localhost:3306/hobbies')

    for chunk in df_iter :
        t_start = time()

        chunk = chunk

        
        chunk.to_sql(name='full', con=engine, if_exists='append',schema='hobbies',index=False)

        t_end = time()

        print('inserted another chunk, took %.3f second' % (t_end - t_start))

#insert_chunks("full.csv")