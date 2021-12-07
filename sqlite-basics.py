#import sql3, pandas and connect to the databse.
import sqlite3
import pandas as pd
sql_connect = sqlite3.connect("factbook.db")

#activates the cursor
cursor = sql_connect.cursor()

#the SQL query to look at the tables in the databse
q1 = "SELECT * FROM sqlite_master WHERE type='table';"
query = "SELECT * FROM facts;"

#execute the query and read it in pandas, this returns a table in pandas form
database_info = pd.read_sql_query(q1, sql_connect)
print(database_info)
results = cursor.execute(query).fetchall()
print(results)
results_pd=pd.read_sql_query(query,sql_connect)
print(results_pd)
