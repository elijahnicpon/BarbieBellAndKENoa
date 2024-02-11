import os
from pymongo import MongoClient
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import streamlit as st
from langchain_community.vectorstores import MongoDBAtlasVectorSearch

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

if not OPENAI_API_KEY:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

ATLAS_CONNECTION_STRING = os.getenv('ATLAS_CONNECTION_STRING')
if not ATLAS_CONNECTION_STRING:
    raise ValueError("The ATLAS_CONNECTION_STRING environment variable is not set.")

DB_NAME = "langchain"
COLLECTION_NAME = "pt"

if "health_metrics" in st.session_state:


    vector_search = MongoDBAtlasVectorSearch.from_connection_string(
        ATLAS_CONNECTION_STRING,
        f"{DB_NAME}.{COLLECTION_NAME}",
        OpenAIEmbeddings(),
        index_name="vector_index"
    )

    llm = ChatOpenAI(temperature=0.1)
    qa = ConversationalRetrievalChain.from_llm(llm, vector_search.as_retriever())
    # st.chat_message("assistant", avatar="🏋️‍♀️").write("Hello")


    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            # {"role": "system", "content": "you are Barbie Bell, an eccentric olympic trainer, and you’re about to meet your next client. your goal is to collect all relevant information to give them a custom workout plan based on your client's specifications. start by introducing yourself, ask if they're ready to answer questions to generate a workout, then interview your client question by question and ask about them 10-20 questions about their fitness goals, gender, height, weight, health, access to equipment, time availability, whether they want a weekly plan or single day, and anything else to give them a good workout. when you're finished with the interview, neatly summarize the metrics you collected during the interview and call it 'SUMMARY'"},
            {"role": "assistant", "content": "Hi! I'm Barbie Bell, your personal trainer, and I'm thrilled to help you with your fitness goals! Are you ready to get started?"}
        ]

    user_input = st.chat_input("Ask Barbie Bell, your personal trainer, any fitness related question!")

    

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        if message["role"] == "assistant":

            with st.chat_message(message["role"], avatar="🏋️‍♀️"):
                st.markdown(message["content"])
        else:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if len(st.session_state.messages) == 1:
        with st.container():
            st.markdown("#### Sample Prompts :)")
            col1,col2, col3 = st.columns(3)
            with col1:
                if st.button("Create a workout plan for me to do today!"):
                    user_input = "Create a workout plan for me to do today! Feel free to ask 5-10 additional questinos to give a good recommendation."
            with col2:
                if st.button("Create a weeks worth of workout plans please!"):
                    user_input = "Create a weeks worth of workout plans please! Feel free to ask 5-10 additional questinos to give a good recommendation."
            with col3: 
                if st.button("How Can Athletes Improve Force Production?"):
                    user_input = "How Can Athletes Improve Force Production?"

    # Accept user input
    # if prompt := st.chat_input("Ask Barbie Bell, your personal trainer, any fitness related question!"):
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Query the assistant using the latest chat history
        result = qa({"prompt":"you are a helpful elite personal trainer. please help your client create workout plans and answer fitness questions.", "question": user_input, "health_info": st.session_state.health_metrics, "chat_history": [(message["role"], message["content"]) for message in st.session_state.messages]})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            full_response = result["answer"]
            message_placeholder.markdown(full_response + "|")
        message_placeholder.markdown(full_response)    
        print(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        # st.write(st.session_state.health_metrics)
else:
    st.subheader("Please submit your personal information in Home to chat with Barbie Bell!")