# EndeeRAG: RAG System with Endee Vector Database

EndeeRAG is a Retrieval-Augmented Generation (RAG) system that uses the Endee vector database for efficient document storage and retrieval, combined with transformer-based embeddings and language models for question answering.

## Features

- **Vector Storage**: Uses Endee vector database for high-performance similarity search
- **Document Ingestion**: Supports PDF, TXT, and MD file formats with automatic chunking
- **Embedding Generation**: Leverages Sentence Transformers for semantic embeddings
- **RAG Pipeline**: Combines retrieval and generation for accurate question answering
- **REST API**: Provides API endpoints for querying the system

## Prerequisites

- Python 3.8+
- Endee server running on `http://127.0.0.1:8080`
- Required Python packages (see requirements.txt)

## Installation

1. **Clone or navigate to the EndeeRAG directory:**
   ```bash
   cd EndeeRAG
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure Endee server is running:**
   - Start the Endee server on localhost:8080
   - The server should be accessible at `http://127.0.0.1:8080`

## Configuration

Edit `config.py` to customize:
- `EMBEDDING_MODEL`: Sentence transformer model (default: "all-MiniLM-L6-v2")
- `ENDEE_INDEX_PATH`: Path for Endee index storage
- `TOP_K`: Number of top results to retrieve (default: 5)

## Usage

### 1. Test Vector Store Integration

Run the vector store test to verify Endee connectivity:
```bash
python test_vector_store.py
```

### 2. Run Demo Queries

Execute sample queries against the RAG system:
```bash
python demo_queries.py
```

### 3. Interactive Querying

Use the query engine directly:
```bash
python -c "from app.query import RAGQueryEngine; engine = RAGQueryEngine(); print(engine.ask('What is the refund policy?'))"
```

### 4. Document Ingestion

Add documents to the vector store:
```bash
python ingest_docs.py
```

Or programmatically:
```python
from app.ingest import prepare_chunks
from app.embed import generate_embeddings
from app.vector_store import EndeeVectorStore

# Load and chunk documents
chunks = prepare_chunks()
embeddings = generate_embeddings(chunks)

# Store in Endee
store = EndeeVectorStore()
store.add_documents(chunks, embeddings)
```

## Project Structure

```
EndeeRAG/
├── app/
│   ├── __init__.py
│   ├── api.py          # REST API endpoints
│   ├── embed.py        # Embedding generation
│   ├── ingest.py       # Document loading and chunking
│   ├── query.py        # RAG query engine
│   ├── rag.py          # RAG pipeline (if separate from query.py)
│   ├── search.py       # Search functionality
│   └── vector_store.py # Endee vector store integration
├── config.py           # Configuration settings
├── data/
│   └── docs/           # Document storage
├── demo_queries.py     # Demo script
├── endee_index/        # Endee index storage
├── endee_texts.json    # Persisted text mappings
├── ingest_docs.py      # Document ingestion script
├── logs/               # Application logs
├── query_terminal.py   # Terminal query interface
├── requirements.txt    # Python dependencies
├── scripts/            # Utility scripts
├── test_vector_store.py # Vector store tests
├── tests/              # Unit tests
└── TODO.md             # Development tasks
```

## API Endpoints

The system provides REST API endpoints (when api.py is implemented):
- `POST /query`: Submit a question and get an answer
- `POST /ingest`: Add new documents to the system

## Sample Data

The system comes with sample FAQ data including:
- Refund policy information
- Password reset procedures
- Employee onboarding process
- Payment methods
- Warranty information
- Shipping and returns
- Customer support contact

## Troubleshooting

### Common Issues

1. **Connection Error to Endee Server**
   - Ensure Endee server is running on `http://127.0.0.1:8080`
   - Check firewall settings and port availability

2. **Import Errors**
   - Verify all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility

3. **Embedding Model Issues**
   - Ensure internet connection for downloading models
   - Check available disk space for model storage

### Logs

Check the `logs/` directory for detailed error information and system activity.

## Development

### Adding New Features

1. Update `TODO.md` with new tasks
2. Implement changes in appropriate modules
3. Add tests in the `tests/` directory
4. Update documentation in this README

### Testing

Run the test suite:
```bash
python -m pytest tests/
```

