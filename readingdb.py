#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 17:28:43 2021

@author: Clement
"""
import pandas
import sqlite3
import os

current = os.path.dirname(os.path.realpath(__file__))

conn = sqlite3.connect(f'{current}/db.sqlite3')

res = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
for name in res:
    print (name[0])

cursor = conn.cursor()

cursor.execute('SELECT * FROM User')
for row in cursor:
    print(row)
    
cursor.execute('''UPDATE User
               SET email='clement.houzard@grid-tech.fr' 
               WHERE username='clement' ''')
               
cursor.execute('SELECT * FROM User')               
for row in cursor:
    print(row)
    
conn.commit()
conn.close()
#%%
df = pandas.read_sql_query(f"SELECT * from {name[0]}", conn)
df.iloc[0,1] = 'clement.houzard@grid-tech.fr'
print(df)
df.to_sql(name[0], conn)


conn.close()