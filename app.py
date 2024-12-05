from flask import Flask, request, jsonify
from transformers import pipeline
from database import SessionLocal, KnowledgeBase

app = Flask(__name__)

# Load Hugging Face model
chat_model = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B")

# Fetch context from the database
def fetch_context(query):
    session = SessionLocal()
    results = session.query(KnowledgeBase).filter(KnowledgeBase.topic.ilike(f"%{query}%")).all()
    session.close()
    return " ".join([entry.content for entry in results])

# Generate a chatbot response
def generate_response(user_input, context):
    combined_prompt = f"Context: {context}\nUser: {user_input}\nBot:"
    response = chat_model(combined_prompt, max_length=150, num_return_sequences=1)[0]["generated_text"]
    return response.split("Bot:")[-1].strip()

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_input = data.get("query", "").strip()
    if not user_input:
        return jsonify({"error": "No query provided"}), 400

    # Fetch dynamic context from the database
    context = fetch_context(user_input)
    if not context:
        context = "I have no specific knowledge on this topic."

    # Generate response
    response = generate_response(user_input, context)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)