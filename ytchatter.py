from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import  RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

from youtube_urls_validator import validate_url
from pytube import extract
import re
load_dotenv()

class YTChatter:
    def __init__(self):
        self.retriever = None
        self.vector_store = None
        self.parser = StrOutputParser()
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""
            You are a helpful assistant.
            Answer ONLY from the provided transcript context.
            If the context is not sufficient to answer the question, say "I don't know".

            {context}
            Question: {question}
            """,
        )

    def start_chatting(self, vector_store, llm):
        print("Starting chat...")
        self.retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
        self.parallel_chain = RunnableParallel({
            "context": self.retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough()
        })

        self.final_chain = self.parallel_chain | self.prompt_template | llm | self.parser

    def ask_question(self, question):
        if self.retriever is None:
            raise ValueError("You need to start chatting first by calling start_chatting with a video ID.")

        response = self.final_chain.invoke(question)
        return response

def extract_video_id(url):
    try:
        strx = "([A-Za-z0-9._%-]*)(\\&\\S+)?$"
        if re.match(strx, url):
            print("Patterned matched. Returninng videoid", url)
            return url
        validate_url(url)
        video_id = extract.video_id(url)
        print(f"Reeturning extracted Video ID: {video_id} from URL.")
        return video_id
    except Exception as e:
        return None

def get_video_transcript(video_id):
    ytt_api = YouTubeTranscriptApi()
    try:
        print(f"Fetching transcripts for video ID: {video_id}")
        transcripts = ytt_api.get_transcript(video_id, languages=['en', 'en-US', 'en-GB'])
        transcript_text = prepare_transcript(transcripts)
        return transcript_text
    except Exception as e:
        print(f"Error fetching transcripts: {e}")
        return None

def prepare_transcript(transcripts):
    transcripts_text = ' '.join([t["text"] for t in transcripts])
    transcripts_text = transcripts_text.replace('\n', ' ')
    transcripts_text = transcripts_text.replace('  ', ' ')
    transcripts_text = transcripts_text.replace('♪', '')
    return transcripts_text

def create_vector_store(transcript_text, video_id):
    from langchain_openai import OpenAIEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    documents = text_splitter.create_documents([transcript_text])
    embeddings = OpenAIEmbeddings()

    return Chroma.from_documents(
        documents,
        embeddings,
        collection_name=video_id)

def format_docs(retrieved_docs):
    context_text = "\n\n".join([doc.page_content for doc in retrieved_docs])
    return context_text