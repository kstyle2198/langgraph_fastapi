# LangGraph + FastAPI + Streamlit

### Directory Structure

```bash
├── backend
│   ├── server.py
│   └── utils
├── db
│   └── chroma_db_02
└── frontend
    └── app.py

```
- `utils/`: This directory contains the building blocks and utility functions used by the chatbot, such as document retrieval, answer generation, and grading mechanisms.

### Getting Started

To get started with the RAG chatbot for Speckle's developer documentation, follow these steps:

1. Start the server: `python backend/server.py`
2. Run the streamlit app: `streamlit run frontend/app.py`
3. Type your question in the space provided to get a response.

