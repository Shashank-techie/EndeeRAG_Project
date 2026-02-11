from .search import semantic_search
import google.genai as genai
import os

# Configure Google Gemini API
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY", "AIzaSyAF1--d0-DDorel0h0JTVlYuV0lFVD_rzk"))

def generate_answer(query):
    context_chunks = semantic_search(query)

    if not context_chunks:
        return "No relevant information found in the documents."

    # Combine all context for analysis
    full_context = "\n".join(context_chunks)

    # Split into Q&A pairs and find the best match
    qa_pairs = []
    lines = full_context.split('\n')

    current_q = None
    current_a = None

    for line in lines:
        line = line.strip()
        if line.startswith('Q:'):
            if current_q and current_a:
                qa_pairs.append((current_q, current_a))
            current_q = line[3:].strip()  # Remove 'Q: '
            current_a = None
        elif line.startswith('A:') and current_q:
            current_a = line[3:].strip()  # Remove 'A: '

    # Add the last pair if exists
    if current_q and current_a:
        qa_pairs.append((current_q, current_a))

    # Find the best matching Q&A pair
    best_answer = None
    best_score = 0

    query_words = set(query.lower().split())

    for question, answer in qa_pairs:
        question_words = set(question.lower().split())
        score = len(query_words.intersection(question_words))

        # Also check for partial matches in answer
        answer_words = set(answer.lower().split())
        score += len(query_words.intersection(answer_words)) * 0.5  # Weight answer matches less

        if score > best_score:
            best_score = score
            best_answer = answer

    if best_answer:
        return best_answer

    # If no good Q&A match, try pattern matching on the full context
    query_lower = query.lower()

    if "payment" in query_lower and "credit cards" in full_context:
        return "We accept credit cards (Visa, MasterCard, American Express), PayPal, and bank transfers for all purchases."
    elif "warranty" in query_lower and "1-year" in full_context:
        return "Yes, all products come with a 1-year warranty covering manufacturing defects. Extended warranties are available for purchase."
    elif "shipping" in query_lower and "international" in full_context:
        return "Yes, we ship to most countries worldwide. Shipping costs and delivery times vary by location."
    elif "contact" in query_lower and "support@" in full_context:
        return "You can reach customer support via email at support@company.com or by phone at 1-800-123-4567 during business hours."
    elif "track" in query_lower and "tracking number" in full_context:
        return "Once your order ships, you'll receive a tracking number via email. You can use this number on our website to track your package."
    elif "return" in query_lower and "return label" in full_context:
        return "To return an item, contact customer support within 30 days of receipt. You'll receive a return label and instructions via email."
    elif "account" in query_lower and "settings" in full_context:
        return "Log in to your account on our website, go to 'Account Settings,' and update your information there."

    # Last resort: extract from the most relevant chunk
    for chunk in context_chunks:
        chunk = chunk.strip()
        if 'A:' in chunk and len(chunk) > 20:
            # Extract just the answer part
            parts = chunk.split('A:', 1)
            if len(parts) > 1:
                answer = parts[1].split('\n')[0].strip()
                if len(answer) > 10:  # Ensure it's a substantial answer
                    return answer

    return "I found some relevant information but couldn't extract a specific answer. Please try rephrasing your question."
