import os
from pymongo import MongoClient
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain_community.llms import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
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
COLLECTION_NAME = "nutrition"

if "health_metrics" in st.session_state:

    vector_search = MongoDBAtlasVectorSearch.from_connection_string(
        ATLAS_CONNECTION_STRING,
        f"{DB_NAME}.{COLLECTION_NAME}",
        OpenAIEmbeddings(),
        index_name="vector_index"
    )

    llm = ChatOpenAI(temperature=0.1)
    qa = ConversationalRetrievalChain.from_llm(llm, vector_search.as_retriever())

    # Initialize chat history
    if "ken_messages" not in st.session_state:
        st.session_state.ken_messages = [
            # {"role": "system", "content": "you are Barbie Bell, an eccentric olympic trainer, and you’re about to meet your next client. your goal is to collect all relevant information to give them a custom workout plan based on your client's specifications. start by introducing yourself, ask if they're ready to answer questions to generate a workout, then interview your client question by question and ask about them 10-20 questions about their fitness goals, gender, height, weight, health, access to equipment, time availability, whether they want a weekly plan or single day, and anything else to give them a good workout. when you're finished with the interview, neatly summarize the metrics you collected during the interview and call it 'SUMMARY'"},
            {"role": "assistant", "content": "Hi! I'm Kenoa, your personal nutritionist! How can I help you today?"}
        ]

    user_input = st.chat_input("Ask KENoa, your personal nutritionist, any nutrition related question!")

    

    # Display chat messages from history on app rerun
    for message in st.session_state.ken_messages:
        if message["role"] == "assistant":

            with st.chat_message(message["role"], avatar="🧑‍🍳"):
                st.markdown(message["content"])
        else:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if len(st.session_state.ken_messages) == 1:
        with st.container():
            st.markdown("#### Sample Prompts :)")
            col1,col2, col3 = st.columns(3)
            with col1:
                if st.button("What's a healthy meal for me to eat tonight?"):
                    user_input = "What's a healthy meal for me to eat tonight? Ask at least 3-5 questions to give a personalized recommendation."
            with col2:
                if st.button("What foods should I avoid based on my conditions?"):
                    user_input = "What foods should I avoid based on my conditions?"
            with col3: 
                if st.button("What foods can help me recover from a long workout?"):
                    user_input = "What foods can help me recover from a long workout?"

    # Accept user input
    # if prompt := st.chat_input("Ask Barbie Bell, your personal trainer, any fitness related question!"):
    if user_input:
        st.session_state.ken_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        if st.session_state.ken_messages[-1]["role"] != "assistant":

            DB_NAME = "langchain"
            COLLECTION_NAME = "nutrition"

            vector_search = MongoDBAtlasVectorSearch.from_connection_string(
                ATLAS_CONNECTION_STRING,
                f"{DB_NAME}.{COLLECTION_NAME}",
                OpenAIEmbeddings(),
                index_name="vector_index"
            )

            

            context = vector_search.similarity_search_with_score(query=user_input, k=2)

            # Search using cosine similarity
            # results = vector_search.search(query_embedding, limit=1, similarity_metric="cosine")
            # print(results)

            prompt = PromptTemplate(
                input_variables=["chat_history", "bio_info", "context", "question"],
                template=(
                    """You are a very kind and friendly AI personal nutritionist, named KENoa. You are
                    currently having a conversation with a human. Answer the questions
                    in a kind and friendly tone with some sense of humor.
                    
                    chat_history: {chat_history},
                    Human: {question},
                    human's info: {bio_info},
                    context: {context}
                    AI:"""
                )
            )

            llm = ChatOpenAI()
            memory = ConversationBufferWindowMemory(memory_key="chat_history", input_key="question", k=4)
            llm_chain = LLMChain(
                llm=llm,
                memory=memory,
                prompt=prompt
            )
            with st.chat_message("assistant", avatar="🧑‍🍳"):
                with st.spinner("Loading..."):
                    # ai_response = llm_chain.predict(question=user_input, biometric_info=st.session_state.health_metrics)
                    ai_response = llm_chain.predict(question=user_input,bio_info=st.session_state.health_metrics, context=context)
                    st.write(ai_response)
            new_ai_message = {"role": "assistant", "content": ai_response}
            st.session_state.ken_messages.append(new_ai_message)
        

        # Query the assistant using the latest chat history
        # result = qa({"prompt":"you are a helpful personal nutritionist. please help your client create nutrition plans and answer nutrition questions in english.", "question": user_input, "health_info": st.session_state.health_metrics, "chat_history": [(message["role"], message["content"]) for message in st.session_state.ken_messages]})

        # # Display assistant response in chat message container
        # with st.chat_message("assistant"):
        #     message_placeholder = st.empty()
        #     full_response = ""
        #     full_response = result["answer"]
        #     message_placeholder.markdown(full_response + "|")
        # message_placeholder.markdown(full_response)    
        # # print(full_response)
        # st.session_state.ken_messages.append({"role": "assistant", "content": full_response})
        # # st.write(st.session_state.health_metrics)
        # print(f"{[(message['role'], message['content']) for message in st.session_state.ken_messages]}")
else:
    st.subheader("Please submit your personal information in Home to chat with KENoa!")