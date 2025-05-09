import sqlite3
import pyodbc

# This script migrate a SQLite table to a SQL Server table

# Connecting SQLite
sqlite_conn = sqlite3.connect("C:/yourpath/archive.sqlite")
sqlite_cursor = sqlite_conn.cursor()
table = 'test'

# Reading table in SQLite
sqlite_cursor.execute(f"SELECT * FROM {table}")
data_table = sqlite_cursor.fetchall()
columns = [desc[0] for desc in sqlite_cursor.description]

# Conexão com SQL Server
sql_server_conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=yourServer;'
    'DATABASE=yourDataBase;'
    'UID=userID;'
    'PWD=Password'
)
sql_server_cursor = sql_server_conn.cursor()

# Inserting in SQL Server
insert_sql = f"""
    INSERT INTO {table} ({', '.join(columns)})
    VALUES ({', '.join(['?'] * len(columns))})
"""

for line in data_table:
    sql_server_cursor.execute(insert_sql, line)

sql_server_conn.commit()

# Closing connections
sqlite_conn.close()
sql_server_conn.close()

print(f"Table '{table}' transfered successfully.")
