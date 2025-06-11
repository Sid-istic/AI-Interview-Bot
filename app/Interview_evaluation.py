import google.generativeai as genai
from dotenv import load_dotenv
import json
import os

load_dotenv


def generate_evaluation(history_file: str) -> str:

    with open(history_file, 'r') as f:
        history = json.load(f)
    
    # Prepare conversation history for analysis
    conversation = "\n".join(
        f"{msg['role'].upper()}: {msg['content']}" 
        for msg in history
    )
    
    # Initialize Gemini
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Analyze this technical interview conversation and provide:
    
    1. Brief overall assessment (1 paragraph)
    2. Technical knowledge score (0-10)
    3. Communication skills score (0-10)
    4. Problem-solving score (0-10)
    5. Top 3 specific improvement suggestions
    
    Format your response in Markdown with clear headings.
    
    Conversation:
    {conversation}
    """
    
    response = model.generate_content(prompt)
    return response.text

# Modified save function that also generates evaluation
def save_and_evaluate():
    filename = 'chat_history.json'
    evaluation = generate_evaluation(filename)
    print("\n=== AI Evaluation ===")
    print(evaluation)
    
    # Also save evaluation to file
    eval_filename = filename.replace('.json', '_eval.md')
    with open(eval_filename, 'w') as f:
        f.write(evaluation)
    print(f"Evaluation saved to {eval_filename}")

