from .rag import generate_answer

class RAGQueryEngine:
    def __init__(self):
        # Initialize any necessary components if needed
        pass

    def ask(self, query):
        return generate_answer(query)
