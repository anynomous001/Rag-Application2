# RAG Application with LangChain and Gemini

This is a Retrieval Augmented Generation (RAG) application that uses LangChain, Google's Gemini model, and ChromaDB to provide intelligent responses based on document content.

## Features

- PDF document loading and processing
- Text chunking with recursive character splitting
- Document embedding using Google's Generative AI
- Vector storage with ChromaDB
- Interactive query system with context-aware responses
- Integration with Google's Gemini 1.5 Pro model

## Prerequisites

- Python 3.x
- Google API key (for Gemini model access)

## Required Packages

```bash
pip install langchain-community
pip install langchain-google-genai
pip install chromadb
pip install python-dotenv
pip install pypdf
```

## Environment Setup

1. Create a `.env` file in the project root
2. Add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

1. Place your PDF document in an accessible location
2. Update the `file_path` variable in `webLoader.py` to point to your PDF
3. Run the application:
```bash
python webLoader.py
```

## How it Works

1. **Document Loading**: The application loads a PDF document using LangChain's PyPDFLoader
2. **Text Processing**: Content is split into manageable chunks using RecursiveCharacterTextSplitter
3. **Embedding**: Text chunks are converted to embeddings using Google's Generative AI
4. **Vector Storage**: Embeddings are stored in ChromaDB for efficient retrieval
5. **Query Processing**: User queries are processed against the stored documents
6. **Response Generation**: Gemini model generates contextual responses based on retrieved documents

## Interactive Query System

The application runs in an interactive loop where you can:
- Enter questions about the document content
- Receive AI-generated responses based on the document context
- Type 'quit' to exit the application

## Configuration

Key parameters can be adjusted in the code:
- `chunk_size`: Size of text chunks (default: 2000)
- `chunk_overlap`: Overlap between chunks (default: 100)
- `search_kwargs`: Number of similar documents to retrieve (default: k=2)
- LLM temperature: Controls response creativity (default: 0.2)

## Notes

- The system is currently configured to work with "The Almanack of Naval Ravikant" PDF
- Responses are generated based on document content only
- The assistant (Cal) will indicate if the context is insufficient to answer a question