# BM25 Vector-less RAG

A Retrieval-Augmented Generation (RAG) system built with FastAPI,
Oracle Database, BM25 lexical retrieval, and Groq LLMs.

## Overview

This project implements a vector-less RAG pipeline for document
question answering.

Unlike vector-based RAG systems, this project does not use embeddings
or a vector database. Instead, it uses the BM25 ranking algorithm to
retrieve the most relevant document chunks based on lexical matching.

## Architecture

```text
Document Upload
      ↓
Text Extraction
      ↓
Text Chunking
      ↓
Oracle Database
      ↓
BM25 Retrieval
      ↓
Relevant Chunks
      ↓
Groq LLM
      ↓
Generated Answer
```

## Tech Stack

- Python
- FastAPI
- Oracle Database
- BM25
- Groq API
- Pydantic
- Uvicorn

## Project Structure

```text
backend/
├── app/
│   ├── api/
│   │   ├── admin_routes.py
│   │   ├── chat_routes.py
│   │   ├── document_routes.py
│   │   └── session_routes.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   │
│   ├── repositories/
│   │   ├── chat_repository.py
│   │   ├── chunk_repository.py
│   │   ├── document_repository.py
│   │   └── session_repository.py
│   │
│   ├── schemas/
│   │   ├── chat_schema.py
│   │   ├── document_schema.py
│   │   └── response_schema.py
│   │
│   ├── services/
│   │   ├── chat_service.py
│   │   ├── document_service.py
│   │   ├── llm_service.py
│   │   └── retrieval_service.py
│   │
│   ├── utils/
│   │   ├── docx_reader.py
│   │   ├── pdf_reader.py
│   │   ├── text_chunker.py
│   │   └── text_reader.py
│   │
│   └── main.py
│
├── tests/
│   └── test_pdf.py
│
├── requirements.txt
└── .env.example
```

## Key Features

- Document upload
- PDF, DOCX, and TXT text extraction
- Text chunking
- Oracle Database storage
- BM25-based document retrieval
- LLM-based answer generation
- Chat and session management
- REST API using FastAPI
- Interactive API documentation with Swagger UI

## Retrieval Approach

BM25 is used as the lexical retrieval algorithm.

When a user submits a question, the system compares the query terms
against the indexed document chunks and calculates a relevance score
for each chunk.

The highest-scoring chunks are selected as context and passed to the
Groq LLM to generate the final answer.

```text
User Query
    ↓
Query Processing
    ↓
BM25 Scoring
    ↓
Top Relevant Chunks
    ↓
Context Construction
    ↓
Groq LLM
    ↓
Final Answer
```

## Database

This project uses Oracle Database to store:

- Document metadata
- Document chunks
- Chat history
- Session information

The Oracle Database instance is not included or hosted with this
repository.

You must configure your own Oracle Database instance to run the
complete application.

## Environment Variables

Create a `.env` file inside the `backend/` directory.

```
ORACLE_USER=your_username
ORACLE_PASSWORD=your_password
ORACLE_DSN=your_dsn

GROQ_API_KEY=your_api_key
GROQ_MODEL=your_model
```

Never commit your `.env` file or API keys to GitHub.

## Installation

Clone the repository:

```
git clone <repository-url>
```

Navigate to the backend:

```
cd backend
```

Create a virtual environment:

```
python -m venv venv
```

Activate the virtual environment on Windows:

```
venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Configure your `.env` file with the required Oracle Database and
Groq API credentials.

Start the FastAPI server:

```
python -m uvicorn app.main:app --reload
```

The API will be available locally through the FastAPI server.

Swagger API documentation:

```
http://127.0.0.1:8000/docs
```

## Deployment

This project is currently configured for local execution because it
depends on an Oracle Database instance that is not deployed with the
application.

The source code and complete application architecture are available
in this repository for development and experimentation.

## Limitations

- Retrieval is based on lexical matching rather than semantic embeddings.
- Requires an accessible Oracle Database instance.
- Requires a Groq API key for LLM generation.
- The application is currently intended for local execution.

## Future Improvements

- Hybrid BM25 + vector retrieval
- Reranking
- Agentic retrieval
- Streaming LLM responses
- Cloud database deployment
- Improved document indexing
