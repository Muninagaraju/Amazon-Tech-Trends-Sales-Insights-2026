import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Raju2003",
    database="Project2"
)

cursor = conn.cursor()
