from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
import os
from openai import OpenAI
from chat_logic.persona import (
    get_random_persona, 
    get_level_guidelines,
    get_introduction_by_language
)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI client
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.openai.com/v1"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/initialize-chat', methods=['POST'])
def initialize_chat():
    try:
        data = request.json
        language = data.get('language')
        gender = data.get('gender')
        level = data.get('level')
        topic = data.get('topic')
        
        # Get VTuber persona
        persona = get_random_persona(gender, language)
        
        # Get level guidelines
        guidelines = get_level_guidelines(level)
        
        # Create system prompt with strict language level enforcement
        system_prompt = f"""You are {persona['name']}, a {persona['age']}-year-old VTuber who is {persona['personality']} and enjoys {persona['hobby']}.

STRICT LANGUAGE RULES FOR {level} LEVEL:
1. Vocabulary: {guidelines['vocabulary']}
2. Grammar: {guidelines['grammar']}
3. Topics: {guidelines['topics']}

Example phrases for your level: {', '.join(guidelines['examples'][language])}

ADDITIONAL RULES:
- ONLY respond in {language}
- NEVER use vocabulary or grammar above {level} level
- Stay in character as a {persona['personality']} VTuber
- If user uses complex language, respond using only {level} level language
- Maintain conversation about: {topic}

Remember: Your primary role is to help the user practice {language} at {level} level."""

        # Get appropriate introduction for language and level
        introduction = get_introduction_by_language(language, persona, topic, level)
        
        # Store chat information in session
        session['messages'] = [
            {"role": "system", "content": system_prompt},
            {"role": "assistant", "content": introduction}
        ]
        session['persona'] = persona
        
        return jsonify({
            'success': True,
            'persona': persona,
            'introduction': introduction
        })
    except Exception as e:
        print(f"Error in initialize_chat: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message')
        messages = session.get('messages', [])
        persona = session.get('persona')
        
        if not messages:
            return jsonify({'error': 'Chat session not initialized'}), 400
        
        # Add user message
        messages.append({"role": "user", "content": message})
        
        # Get response from OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150
        )
        
        assistant_response = response.choices[0].message.content
        
        # Add assistant response to messages
        messages.append({"role": "assistant", "content": assistant_response})
        
        # Update session
        session['messages'] = messages
        
        return jsonify({
            'success': True,
            'response': assistant_response,
            'persona': persona
        })
    except Exception as e:
        print(f"Error in chat: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)