from flask import Flask, request, jsonify, render_template, url_for
from groq import Groq
from dotenv import load_dotenv
from src.prompt import SYSTEM_PROMPT
import os
from datetime import datetime

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

load_dotenv()
client = Groq(api_key=os.environ['GROQ_API_KEY'])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get', methods=['POST'])
def chat():
    try:
        user_input = request.form.get("msg", "").strip()
        
        if not user_input:
            return jsonify({
                "answer": "Please enter a legal question",
                "timestamp": datetime.now().strftime("%H:%M")
            })
        
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            model="llama3-70b-8192",
            temperature=0.3
        )
        
        return jsonify({
            "answer": response.choices[0].message.content,
            "timestamp": datetime.now().strftime("%H:%M")
        })
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            "answer": "**Error**: Our legal engine is currently unavailable. Please try again later.",
            "timestamp": datetime.now().strftime("%H:%M")
        }), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)