from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit

def get_data_from_database():
    db = SQLDatabase.from_uri("sqlite:////Users/main/Desktop/database/llm.db")
    return db