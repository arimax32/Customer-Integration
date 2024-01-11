import mysql.connector

database = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'yG92*rkl'
)

cursorObject = database.cursor()

#strongmin
cursorObject.execute("create database Customer")