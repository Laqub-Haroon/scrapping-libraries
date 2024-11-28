import sqlite3
import streamlit as st
import pandas as pd
st.set_page_config(layout="wide")
db_name = "libraries_data.db"

if "selected_state" not in st.session_state:
    st.session_state.selected_state = None

connection = sqlite3.connect(db_name)
state_names = [row[0] for row in connection.execute("SELECT state_name FROM states").fetchall()]

if st.session_state.selected_state is None:
    state = st.selectbox("Choose a State", ["Select"] + state_names)
    if state != "Select":
        st.session_state.selected_state = state
        st.experimental_rerun()
else:
    selected_state = st.session_state.selected_state
    st.title(f"Libraries in {selected_state}")

    query = '''
    SELECT libraries.city, libraries.library, libraries.address, libraries.zip, libraries.phone
    FROM libraries
    JOIN states ON libraries.state_id = states.id
    WHERE states.state_name = ?
    '''
    result = pd.read_sql_query(query, connection, params=(selected_state,))

    if result.empty:
        st.write(f"No libraries found for {selected_state}.")
    else:
        st.dataframe(result, use_container_width=True)

connection.close()
