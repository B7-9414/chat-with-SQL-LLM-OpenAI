# from dotenv import load_dotenv

# from langchain_community.agent_toolkits import create_sql_agent
# from langchain_openai import ChatOpenAI
# from langchain_community.utilities.sql_database import SQLDatabase
# from langchain_experimental.sql import SQLDatabaseChain
# from langchain.chains import create_sql_query_chain

# load_dotenv()

# db = SQLDatabase.from_uri("sqlite:///C:\\Users\\admin\\Desktop\\cloud-computing-kata\\local_multimodal_ai_chat\\chat_sessions\\chat_sessions.db")

# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# chain = create_sql_query_chain(llm, db)
# response = chain.invoke({"question": "List 2 messages ?"})
# response

import os
import base64
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from diagram import generate_er_diagram
from langchain.chains import create_sql_query_chain
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities.sql_database import SQLDatabase

load_dotenv()

# Get the database file path from the environment variable
database_file = os.getenv("DATABASE_FILE")

# Initialize SQLDatabase
db = SQLDatabase.from_uri(f"sqlite:///{database_file}")

# Initialize ChatOpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
sql_query_chain = create_sql_query_chain(llm, db)
# response = chain.invoke({"question": "List 2 messages ?"})
# response


# Define function to interact with chatbot
def chat(message):
    response = agent_executor.invoke(message)
    return response

def sql_query_chat(message):
    response = agent_executor.invoke({"question": message})
    return response

# Initialize chat history list
chat_history = []

# Streamlit UI
st.title("MD Database For Developer Team 📊🩺👨‍💻")
tab_titles = [
    "Results",
    "Query",
    "Diagram",
]
tabs = st.tabs(tab_titles)

# Generate ER diagram
output_file = 'erd_diagram.png'
generate_er_diagram(database_file, output_file)


with tabs[0]:
    user_input = st.text_input("You:", "")
    if st.button("Send"):
        response = chat(user_input)
        formatted_response = response['output']
        chat_history.append((user_input, formatted_response))

        # Display chat history
        st.write("Chat History:")
        for entry in chat_history:
            st.write(f"User Input: {entry[0]}")
            st.write(f"Chatbot Response: {entry[1]}")
            st.write("--------------------")
        # Display formatted chatbot responses in a nice table
        st.write("Formatted Chatbot Responses:")
        chat_df = pd.DataFrame(chat_history, columns=['User Input', 'Chatbot Response'])
        st.dataframe(chat_df)

# Query tab
# with tabs[1]:
#     for entry in chat_history:
#         print(sql_query_chain({entry[0]}))
#         st.write(sql_query_chain, {entry[0]})

# Query tab
with tabs[1]:
    for entry in chat_history:
        response = sql_query_chain.invoke({"question": entry[0]})
        st.write(response)
# Diagram tab
with tabs[2]:  # Change to tabs[2]
    st.write("Click the button below to generate and display the Entity-Relationship Diagram.")

    # Check if the diagram file exists
    output_file = 'erd_diagram.png'
    if os.path.exists(output_file):
        # Display the rendered ER diagram
        st.image(output_file, caption='Entity-Relationship Diagram')
    else:
        st.warning("The ER diagram has not been generated yet.")

    if st.button("Generate/Regenerate ER Diagram"):
        # Generate or regenerate ER diagram
        generate_er_diagram()

        # Check if the diagram file exists again after generation
        if os.path.exists(output_file):
            # Display the rendered ER diagram
            st.image(output_file, caption='Entity-Relationship Diagram')

    # Allow the user to save the diagram
    st.write("Download the diagram:")
    with open(output_file, "rb") as file:
        diagram_bytes = file.read()
    diagram_b64 = base64.b64encode(diagram_bytes).decode()
    download_link = f'<a href="data:image/png;base64,{diagram_b64}" download="erd_diagram.png">Download ER Diagram</a>'
    st.markdown(download_link, unsafe_allow_html=True)
