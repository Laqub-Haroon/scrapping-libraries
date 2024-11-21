import sqlite3
import streamlit as st
import pandas as pd

db_name = "libraries_data.db"
connection = sqlite3.connect(db_name)


st.title("Public Library")


state = st.selectbox("Select a State", 
                     [row[0] for row in connection.execute("SELECT DISTINCT state FROM libraries").fetchall()])




query = '''
SELECT city, library, address, zip, phone
FROM libraries
WHERE state = ?
'''
resut = pd.read_sql_query(query, connection, params=(state,))

st.write(f"Showing librares in {state}:")
st.dataframe(resut)

connection.close()

