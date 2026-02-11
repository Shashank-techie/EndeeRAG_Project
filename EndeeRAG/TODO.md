# TODO: Make RAG System Functional

- [x] Update requirements.txt: Add fastapi, google-generativeai, uvicorn
- [x] Fix imports in embed.py: Use absolute import from config
- [x] Fix vector_store.py: Import config, use constants
- [x] Fix search.py: Use EndeeVectorStore instance, fix return format
- [x] Fix rag.py: Update to Google Gemini API with provided key
- [x] Fix api.py: Use absolute import from rag
- [x] Test embedding: Works, dim 384
- [ ] Test vector store (requires Endee server running)
- [ ] Test API
