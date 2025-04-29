import streamlit as st
from ytchatter import YTChatter, extract_video_id
from langchain_community.chat_message_histories import StreamlitChatMessageHistory

# Initialize the chat message history
chat_history = StreamlitChatMessageHistory()

chatter = YTChatter()

if "conversation" not in st.session_state:
    st.session_state.conversation = []

st.set_page_config(page_title="YT Chatter", page_icon=":guardsman:", layout="wide")

st.write(
    "This is a simple app that allows you to ask questions about a YouTube video and get answers using the OpenAI API."
)

video_info = st.text_input(
    "Enter the YouTube video ID",
    placeholder="Enter the YouTube video URL/ID",
    key="video_id",
)

for message in st.session_state.conversation:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if video_info:
    video_id = extract_video_id(video_info)
    if video_id:
        chatter.start_chatting(video_id)
        question = st.chat_input(
            "Ask a question about the video",
            key="question",
        )
        if question:
            st.chat_message("user").markdown(question)
            st.session_state.conversation.append({"role": "user", "content": question})
            with st.spinner("Thinking..."):
                answer = chatter.ask_question(question)

            with st.chat_message("assistant"):
                st.markdown(answer)
            st.session_state.conversation.append({"role": "assistant", "content": answer})
    else:
        st.error("Invalid YouTube URL or video ID. Please enter a valid one.")
else:
    if "video_id" not in st.session_state:
        st.session_state.video_id = ""
