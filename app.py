import streamlit as st
import ytchatter
from ytchatter import YTChatter


video_id="hF-7eKtzAHM"
chatter = YTChatter()

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
    st.chat_input(
        "Ask a question about the video",
        key="question",
    )
else:
    if "video_id" not in st.session_state:
        st.session_state.video_id = ""
