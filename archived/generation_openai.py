from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Setup the Client (Assuming you have your API key set as an environment variable)
client = OpenAI()

def generate_answer(query, retrieved_context):
    """
    The Generation Step: Combining Context + Query into a formatted prompt.
    """
    system_prompt = """
    You are a helpful AI assistant. Answer the user's question ONLY using 
    the provided context. If the answer is not in the context, say 
    'I do not have enough information to answer this.' 
    Do not use your own internal knowledge.
    """
    
    # This is the 'Augmentation' part of RAG
    user_prompt = f"""
    Context:
    {retrieved_context}
    
    Question: 
    {query}
    
    Answer:
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",  #model
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0  # Set to 0 to ensure factual, consistent answers
    )
    
    return response.choices[0].message.content

# --- TEST IT ---
# (Using the parent_text we retrieved in Phase 3.2)
mock_context = """
The Intern CEO leadership framework is built on three pillars: Radical Ownership, 
Systems Thinking, and the Growth Mindset. Radical Ownership means taking 100% 
responsibility for outcomes...
"""

query = "What are the three pillars of the Intern CEO framework?"
answer = generate_answer(query, mock_context)

print(f"User Question: {query}")
print(f"AI Answer: {answer}")