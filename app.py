from langchain_openai import ChatOpenAI
import streamlit as st
from ytchatter import YTChatter, extract_video_id, get_video_transcript, create_vector_store
from langchain_community.chat_message_histories import StreamlitChatMessageHistory

from dotenv import load_dotenv
load_dotenv()

# Initialize the chat message history
chat_history = StreamlitChatMessageHistory()

chatter = YTChatter()

if "chatter" not in st.session_state:
    st.session_state.chatter = chatter

if "llm" not in st.session_state:
    st.session_state.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

if "conversation" not in st.session_state:
    st.session_state.conversation = []

st.set_page_config(page_title="YT Chatter", page_icon=":guardsman:", layout="wide")

st.write(
    "This is a simple app that allows you to ask questions about a YouTube video and get answers using the OpenAI API."
)

if "video_id" not in st.session_state:
    st.session_state.video_id = ""

video_info = st.text_input(
    "Enter the YouTube video ID",
    placeholder="Enter the YouTube video URL/ID",
    key="video_info",
)

for message in st.session_state.conversation:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if video_info:
    
    video_id = extract_video_id(video_info)
    if video_id:
        if video_id != st.session_state.video_id:
            st.session_state.video_id = video_id
            st.session_state.canChat = False
            st.session_state.conversation = []

            transcripts = get_video_transcript(video_id)

            if transcripts:
                vector_store = create_vector_store(transcripts, st.session_state.video_id)
                st.session_state.chatter.start_chatting(vector_store, st.session_state.llm)
                st.session_state.canChat = True
            else:
                st.session_state.canChat = False
            
        if st.session_state.canChat:
            question = st.chat_input(
                "Ask a question about the video",
                key="question",
            )
            if question:
                st.chat_message("user").markdown(question)
                st.session_state.conversation.append({"role": "user", "content": question})
                with st.spinner("Thinking..."):
                    answer = st.session_state.chatter.ask_question(question)

                with st.chat_message("assistant"):
                    st.markdown(answer)
                    st.session_state.conversation.append({"role": "assistant", "content": answer})
        else:
            st.error("Could not retrieve information for the provided video ID.")
    else:
        st.error("Invalid YouTube URL or video ID. Please enter a valid one.")
else:
    if "video_id" not in st.session_state:
        st.session_state.video_id = ""
