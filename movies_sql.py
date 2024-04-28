import streamlit as st
import os
import pandas as pd

from gemini import get_response_from_gemini
from sql_utils import execute_sql_query, get_schema

def find_path(path):
    return os.path.exists(path)

## Prompt -------------------------------------------------------------------------------------------------
sql_prompt = """You are an expert in converting question to SQL query.
schema : {{schema}}
Question: {{question}}
"""

## streamlit app-------------------------------------------------------------------------------------------

st.set_page_config(page_title="Retrieve Any SQL Query")
st.header("Model For Retrieve Data From SQL Database.")

side = st.sidebar.title("Path Of The Database")

database_path= st.sidebar.text_input("Enter The Path")
if find_path(database_path):
    st.sidebar.success("file exist")
    schemas = get_schema(database_path)
    question = st.text_input("Input : ", key="question")
    # st.write(question)
    if question:
        prompt = sql_prompt.replace("{{schema}}",schemas).replace("{{question}}",question)
        sql_query = get_response_from_gemini(prompt)
        st.markdown(sql_query)
        sql_query = sql_query.strip("```sql")
    # print("Response", response)
        response = execute_sql_query(sql_query, database_path)
        st.dataframe(response)
        
else:
    st.sidebar.error("File not found")

