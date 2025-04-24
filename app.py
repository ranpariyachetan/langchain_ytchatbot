import ytchatter
from ytchatter import YTChatter


video_id="hF-7eKtzAHM"
chatter = YTChatter()
chatter.start_chatting(video_id)

question = "What is the main topic of the video?"
res = chatter.ask_question(question)

print(res)