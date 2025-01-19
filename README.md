### Directory Structure

- `app/`: This directory contains the server code `server.py` and the client code `client.py` for running the chatbot application.
  To start the server, run

```
python app/server.py
```

Then, to start the streamlit app, open another terminal and run

```
streamlit run app/client.py
```

backend docker image build
```
docker build . -t langgraph_fastapi
```


- `utils/`: This directory contains the building blocks and utility functions used by the chatbot, such as document retrieval, answer generation, and grading mechanisms.

### Getting Started

To get started with the RAG chatbot for Speckle's developer documentation, follow these steps:

1. Start the server: `python app/server.py`
2. Run the streamlit app: `streamlit run app/client.py`
3. Type your question in the space provided to get a response.

