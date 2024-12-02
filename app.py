import sqlite3
import streamlit as st
import pandas as pd
st.set_page_config(page_title="Public Libraries Directory", layout="wide")
db_name = "libraries_data.db"
connection = sqlite3.connect(db_name)
state_names = [row[0] for row in connection.execute("SELECT state_name FROM states").fetchall()]
st.markdown(
    """
    <style>
        .header-title {
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 10px;
            text-align: center;
        }
        .sub-header {
            font-size: 16px;
            text-align: center;
            color: #555555;
        }
        .state-button {
            display: block;
            margin: 20px auto;
            padding: 10px 20px;
            background-color: #007BFF;
            color: white;
            text-align: center;
            text-decoration: none;
            font-size: 16px;
            border-radius: 5px;
            width: 200px;
        }
        .state-button:hover {
            background-color: #0056b3;
        }
    </style>
    <div>
        <div class="header-title">Public Libraries</div>
        <div class="sub-header">Promoting local public libraries since 1999</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if "selected_state" not in st.session_state:
    st.session_state.selected_state = None
if st.session_state.selected_state is None:
    state = st.selectbox("Choose a State", ["Select"] + state_names)
    if state != "Select":
        st.session_state.selected_state = state
        st.experimental_rerun()
else:
    selected_state = st.session_state.selected_state
    st.markdown(f"<h3 style='text-align:center;'>Libraries in {selected_state}</h3>", unsafe_allow_html=True)
    query = '''
    SELECT libraries.city, libraries.library, libraries.address, libraries.zip, libraries.phone
    FROM libraries
    JOIN states ON libraries.state_id = states.id
    WHERE states.state_name = ?
    '''
    result = pd.read_sql_query(query, connection, params=(selected_state,))
    if result.empty:
        st.write(f"<p style='text-align:center;'>No libraries found for {selected_state}.</p>", unsafe_allow_html=True)
    else:
        st.dataframe(result, use_container_width=True)

connection.close()
