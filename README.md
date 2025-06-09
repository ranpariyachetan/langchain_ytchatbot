This repository was created as part of learning how to create RAG using langchain thru [Youtube video](https://www.youtube.com/watch?v=J5_-l7WIO_w) from [CampusX channel](https://www.youtube.com/@campusx-official).

### Run on local machine
1. Create .env file.
2. Add variable `OPENAI_API_KEY` with correct value in the file.
3. Run command `pip install -r requirements.txt`
4. Run command `stremlit run app.py`
5. Browse `http://localhost:8501` in browser.


### Build docker image
1. Run command `docker build -t ytchatter:latest .`


### Run container from the image
1. Run command `docker run -e OPENAI_API_KEY=<<openaiapikey>> -p 8501:8501 ytchatter:latest`
    1. Replace `<<openaiapikey>>` with a valid OpenAI Api key in the above command.
2. Browse `http://localhost:8501` in browser.

### How to use the application.
1. Browse `http://localhost:8501` in browser.
2. Enter YouTube video id or YouTube Video URL in the input box and hit Enter.
3. Start chatting by asking questions about the video.