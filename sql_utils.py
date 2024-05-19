import sqlite3 
import pandas as pd



# function to retrieve query from database
def execute_sql_query(sql_query, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    try:
        cur.execute(sql_query)
        rows = cur.fetchall()
        headers = [i[0] for i in cur.description]
        conn.close()
        if rows :
            # rows.insert(0,headers)
            df = pd.DataFrame(rows, columns=headers)
            return df
    except sqlite3.Error as e:
        # Error occurred during execution
        print(f"Error executing query: {e}")
        raise


## schema of the tables that are in database
def get_schema(db: str) -> str:
    """Retrieves schema information for a given table.
    
    Parameters:
    db: database file path.

    Returns:
    str: Schemas of all tables.
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute("SELECT name, sql FROM sqlite_master WHERE type='table'")
    schema_data = cur.fetchall()
    conn.close()

    all_schemas_string = ""
    for table_name, schema_sql in schema_data:
        #all_schemas_string += f"Table: {table_name}\n"
        all_schemas_string += f"{schema_sql}\n"
    schema = all_schemas_string.replace("CREATE TABLE"," ")
   

    return schema