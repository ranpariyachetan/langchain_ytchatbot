import streamlit as st
from ytchatter import YTChatter
from langchain_community.chat_message_histories import StreamlitChatMessageHistory

# Initialize the chat message history
chat_history = StreamlitChatMessageHistory()

chatter = YTChatter()

st.session_state.conversation = []

st.set_page_config(page_title="YT Chatter", page_icon=":guardsman:", layout="wide")

st.write(
    "This is a simple app that allows you to ask questions about a YouTube video and get answers using the OpenAI API."
)

video_id = st.text_input(
    "Enter the YouTube video ID",
    placeholder="Enter the YouTube video ID",
    key="video_id",
)

if video_id:
    chatter.start_chatting(video_id)
    question = st.chat_input(
        "Ask a question about the video",
        key="question",
    )
    if question:
        st.session_state.conversation.append({"role": "user", "content": question})
        with st.spinner("Thinking..."):
            answer = chatter.ask_question(question)
        st.session_state.conversation.append({"role": "assistant", "content": answer})
        
        for message in st.session_state.conversation:
            if message["role"] == "user":
                st.chat_message("user").markdown(message["content"])
            else:
                st.chat_message("assistant").markdown(message["content"])
    
else:
    if "video_id" not in st.session_state:
        st.session_state.video_id = ""
