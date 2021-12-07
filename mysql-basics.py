
# This script will show basic commands on mysql, you must have 
# a mysql server running on your machine and adapt the user
# and password.

# we will use mostly mysql connector which is official plugin from mysql
# most of the examples are based on w3school material available at:
# https://www.w3schools.com/python/python_mysql_join.asp
import mysql.connector

# connection details enter here
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="pass"
)
print(mydb)

mycursor = mydb.cursor()

# To create a new database
mycursor.execute("CREATE DATABASE mydatabase")
# If you run the code above again you will get an error because
# database has already been created, use instead:
# mycursor.execute("CREATE DATABASE IF EXISTS mydatabase")
# to not throw error.

# To create a new user and grant it privileges.
mycursor.execute("CREATE USER IF NOT EXISTS 'myuser'@'localhost' IDENTIFIED BY 'pass2';")
mycursor.execute("GRANT ALL PRIVILEGES ON * . * TO 'myuser'@'localhost';")

# Show databases with command:
mycursor.execute("SHOW DATABASES")
for x in mycursor:
  print(x)
print("-- end show databases --")

# connect to a specific database previously created
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="161192r",
  database="mydatabase"
)
mycursor = mydb.cursor()


## create table
mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")
# to delete the table just created use drop table.
mycursor.execute("DROP TABLE IF EXISTS customers")

# Now we will create a column with a unique key for each record, that is a PRIMARY KEY.
# The statement "INT AUTO_INCREMENT PRIMARY KEY" will insert a unique number for each record. 
# Starting at 1, and increased by one for each record.
mycursor.execute("CREATE TABLE customers ( id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")

# now lets add column using the ALTER command
# we need to delete the table just created using drop table. Otherwise
# the CREATE command will throw an error. IF EXISTS allows to avoid error
# in case the table was not created.
mycursor.execute("DROP TABLE IF EXISTS customers") 
# we could also use alter after create table
# create table
mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")
# insert new column in table with alter
mycursor.execute("ALTER TABLE customers ADD COLUMN ( id INT AUTO_INCREMENT PRIMARY KEY)")

# show table
mycursor.execute("SHOW TABLES")
for x in mycursor:
  print(x)

# lets insert a single data row in the customers table
# we will use the INSERT INTO command in the table.
sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
val = ("John", "Highway 21")
mycursor.execute(sql, val)

# then the commit command is required to make the changes, 
# otherwise no changes are made to the table.
mydb.commit()  
print(mycursor.rowcount, "record inserted.")

# now lets insert multiple rows of data in the table with the command executemany()
sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
val = [
  ('Peter', 'Lowstreet 4'),
  ('Amy', 'Apple st 652'),
  ('Hannah', 'Mountain 21'),
  ('Michael', 'Valley 345'),
  ('Sandy', 'Ocean blvd 2'),
  ('Betty', 'Green Grass 1'),
  ('Richard', 'Sky st 331'),
  ('Susan', 'One way 98'),
  ('Vicky', 'Yellow Garden 2'),
  ('Ben', 'Park Lane 38'),
  ('William', 'Central st 954'),
  ('Chuck', 'Main Road 989'),
  ('Viola', 'Sideway 1633')
]
# executemany command is necessary to insert all these records
mycursor.executemany(sql, val)
mydb.commit()
print(mycursor.rowcount, "was inserted.")

# to actually see the entries in the table we have to use SELECT command.
mycursor.execute("SELECT * FROM customers")
# fetchall() command will take all entries from select to be printed
myresult = mycursor.fetchall()

print("---- Results from selection: ----")
for x in myresult:
  print(x)

# to filter our selection we use the WHERE statement
sql = "SELECT * FROM customers WHERE address ='Park Lane 38'"

mycursor.execute(sql)
myresult = mycursor.fetchall()
print("---- Results from filter: ----")
for x in myresult:
  print(x)

# Using LIKE and '%' wildcard to select the records that start, 
# include, or end with a given letter or phrase.
mycursor = mydb.cursor()

sql = "SELECT * FROM customers WHERE address LIKE '%way%'"

mycursor.execute(sql)
myresult = mycursor.fetchall()
print("---- Results containing 'way': ----")
for x in myresult:
  print(x)

# Query values should be escaped to prevent SQL injection, that is
# misuse of SQL commands for hacking.
sql = "SELECT * FROM customers WHERE address = %s"
adr1=input('What address are you looking for? Insert please: ')
adr = (adr1,) 
mycursor.execute(sql, adr)
myresult = mycursor.fetchall()
print("---- Results containing %s: ----"%adr1)
for x in myresult:
  print(x)

# ORDER BY is used to sort the result in ascending or descending order.
sql = "SELECT * FROM customers ORDER BY name"
mycursor.execute(sql)
myresult = mycursor.fetchall()
print("---- Results ordered by name: ----")
for x in myresult:
  print(x)

# DESC is used to order in descending order.
sql = "SELECT * FROM customers ORDER BY name DESC"
mycursor.execute(sql)
myresult = mycursor.fetchall()
print("---- Results ordered by name, inverse alphabetic order: ----")
for x in myresult:
  print(x)

# To delete records from table we use DELETE statement.
sql = "DELETE FROM customers WHERE name = %s"
# !! we always should specify WHERE otherwise every field will be deleted !!
adr1=input('What custormer would you like to delete? Insert name please: ')
adr = (adr1,) 
mycursor.execute(sql,adr)
mydb.commit()
print(mycursor.rowcount, "record(s) deleted")
print("---- Results after deletion : ----")
sql = "SELECT * FROM customers ORDER BY name"
mycursor.execute(sql)
myresult = mycursor.fetchall()
for x in myresult:
  print(x)

# To update existing records in a table the "UPDATE" statement is used
# !! we always should specify WHERE otherwise every field will be updated !!
sql = "UPDATE customers SET address = 'Canyon 123' WHERE address = 'Valley 345'"
mycursor.execute(sql)
mydb.commit()
print(mycursor.rowcount, "record(s) affected")

# To prevent injection the following should be used:
sql = "UPDATE customers SET address = %s WHERE address = %s"
adr_to_subst=input("Which address to substitute? Insert: ")
new_adr=input("Insert new address: ")
val = (new_adr, adr_to_subst)
mycursor.execute(sql, val)
mydb.commit()
print(mycursor.rowcount, "record(s) affected")
print("---- Results after update : ----")
sql = "SELECT * FROM customers ORDER BY name"
mycursor.execute(sql)
myresult = mycursor.fetchall()
for x in myresult:
  print(x)


# Let's see some commands to control the output like LIMIT and OFFSET
# if we want to limit the records returned from the query we use LIMIT:
mycursor.execute("SELECT * FROM customers LIMIT 5")
myresult = mycursor.fetchall()
print("---- First 5 results : ----")
for x in myresult:
  print(x)
# if we want to start our record from a given entry we use OFFSET:
mycursor.execute("SELECT * FROM customers LIMIT 5 OFFSET 2")
myresult = mycursor.fetchall()
print("---- First 5 results from third entry onwards : ----")
for x in myresult:
  print(x)

# Now we will read a sample SQL file.
# however this file is large and we need to change the maximum size of
# the allowed packet, to do this we will change our connection first.
mycursor.execute("SET GLOBAL max_allowed_packet=1073741824;")
mycursor.close() 
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="pass"
)
mycursor = mydb.cursor()
mycursor.execute("DROP DATABASE IF EXISTS newbase")
mycursor.execute("CREATE DATABASE IF NOT EXISTS newbase")
# connect to the specific database we created to insert our file
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="pass",
  database="newbase"
)
mycursor = mydb.cursor()

# now we open the file
file= open('Sample-SQL-File.sql')
sql = file.read()
# And read the data within it. This code was based on:
# https://stackoverflow.com/questions/34275794/how-do-i-import-a-mysql-database-in-a-python-script
for result in mycursor.execute(sql, multi=True):
  if result.with_rows:
    print("Rows produced by statement '{}':".format(
      result.statement))
    print(result.fetchall())
  else:
    print("Number of rows affected by statement '{}': {}".format(
      result.statement, result.rowcount))
mydb.commit()
print("-- Show tables in newbase --")
mycursor.execute("SHOW TABLES")
for x in mycursor:
  print(x)
mydb.close()


# now we are going to use sqlalchemy and pymysql to show
# some examples using the JOIN statement. Additionally,
# we will be creating the table through pandas.
from sqlalchemy import create_engine
import pymysql
import pandas as pd
 
# based on code on https://pythontic.com/pandas/serialization/mysql
users=[{ 'id': 1, 'name': 'John', 'fav': 154},
{ 'id': 2, 'name': 'Peter', 'fav': 154},
{ 'id': 3, 'name': 'Amy','fav': 155},
{ 'id': 4, 'name': 'Hannah', 'fav':''},
{ 'id': 5, 'name': 'Michael', 'fav':''}]
dataFrame1=pd.DataFrame(data=users)
tableName1='users'
print(dataFrame1)
products=[{ 'id': 154, 'name': 'Chocolate Heaven' },
{ 'id': 155, 'name': 'Tasty Lemons' },
{ 'id': 156, 'name': 'Vanilla Dreams' }]
dataFrame2=pd.DataFrame(data=products)
tableName2='products'
print(dataFrame2)
sql_engine = create_engine('mysql+pymysql://root:pass@127.0.0.1/', pool_recycle=3600)
sqlConnection = sql_engine.connect()
## to show databases within sqlalchemy
q = sql_engine.execute('SHOW DATABASES')
available_tables = q.fetchall()
print(available_tables)
## to create and use a new database
sql_engine.execute("DROP DATABASE IF EXISTS test_join") #create db
sql_engine.execute("CREATE DATABASE IF NOT EXISTS test_join") #create db
db_engine = create_engine('mysql+pymysql://root:pass@127.0.0.1/test_join')
dbConnection= db_engine.connect()

## lets define a simple function to insert dataframe in a given database.
def DFtoSQL(dataFrame,tableName,dbConnection):
    try:
        frame = dataFrame.to_sql(tableName, dbConnection);
    except ValueError as vx:
        print(vx)
    except Exception as ex:   
        print(ex)
    else:
        print("Table created successfully.");   
    
    finally:
        select = db_engine.execute("SELECT * FROM %s"%tableName)
        fetch=select.fetchall()
        print(fetch)
DFtoSQL(dataFrame1,tableName1,dbConnection)
DFtoSQL(dataFrame2,tableName2,dbConnection)
dbConnection.close()

# now we will do a JOIN operation on the tables
sql = "SELECT \
  users.name AS user, \
  products.name AS favorite \
  FROM users \
  INNER JOIN products ON users.fav = products.id"
select_inner = db_engine.execute(sql)
result = select_inner.fetchall()
print("-- favorite products by user -- ")
for x in result:
  print(x)

# In the example above, Hannah, and Michael were excluded from the result, 
# that is because INNER JOIN only shows the records where there is a match.
# If you want to show all users, even if they do not have a favorite product, 
# use the LEFT JOIN statement:
sql = "SELECT \
  users.name AS user, \
  products.name AS favorite \
  FROM users \
  LEFT JOIN products ON users.fav = products.id"
select_left = db_engine.execute(sql)
result = select_left.fetchall()
print("-- users and their favorite products -- ")
for x in result:
  print(x)

# If you want to return all products, and the users who have them as their 
# favorite, even if no user have them as their favorite, use the RIGHT JOIN statement:
sql = "SELECT \
  users.name AS user, \
  products.name AS favorite \
  FROM users \
  RIGHT JOIN products ON users.fav = products.id"
select_right = db_engine.execute(sql)
result = select_right.fetchall()
print("-- products and users that have them as favorites -- ")
for x in result:
  print(x)

