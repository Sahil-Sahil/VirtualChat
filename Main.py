import os
from openai import OpenAI
import random
import time

def get_random_persona(gender, language):
    personas = {
        "English": {
            "male": [
                {"name": "James", "age": 28, "occupation": "Software Engineer", "hobby": "playing guitar"},
                {"name": "Michael", "age": 32, "occupation": "Teacher", "hobby": "hiking"},
                {"name": "William", "age": 25, "occupation": "Marketing Specialist", "hobby": "photography"}
            ],
            "female": [
                {"name": "Emma", "age": 27, "occupation": "Journalist", "hobby": "yoga"},
                {"name": "Sarah", "age": 30, "occupation": "Architect", "hobby": "painting"},
                {"name": "Olivia", "age": 24, "occupation": "Chef", "hobby": "traveling"}
            ]
        },
        "German": {
            "male": [
                {"name": "Thomas", "age": 29, "occupation": "Ingenieur", "hobby": "Fußball"},
                {"name": "Markus", "age": 31, "occupation": "Lehrer", "hobby": "Wandern"},
                {"name": "Felix", "age": 26, "occupation": "Künstler", "hobby": "Fotografie"}
            ],
            "female": [
                {"name": "Anna", "age": 28, "occupation": "Ärztin", "hobby": "Klavierspielen"},
                {"name": "Lisa", "age": 25, "occupation": "Designerin", "hobby": "Yoga"},
                {"name": "Julia", "age": 30, "occupation": "Journalistin", "hobby": "Reisen"}
            ]
        }
    }
    return random.choice(personas[language][gender])

def get_language_choice():
    while True:
        print("\n=== Language Selection ===")
        print("1. English")
        print("2. German")
        choice = input("Please select your target language (1/2): ")
        
        if choice == "1":
            return "English"
        elif choice == "2":
            return "German"
        else:
            print("Invalid choice. Please select 1 or 2.")

def get_persona_choice():
    while True:
        print("\n=== Chat Partner Persona ===")
        print("1. Male")
        print("2. Female")
        choice = input("Please select your chat partner's gender (1/2): ")
        
        if choice == "1":
            return "male"
        elif choice == "2":
            return "female"
        else:
            print("Invalid choice. Please select 1 or 2.")

def get_language_level():
    levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
    while True:
        print("\n=== Language Level ===")
        print("Please select your proficiency level:")
        for i, level in enumerate(levels, 1):
            print(f"{i}. {level}")
        
        choice = input(f"Enter your choice (1-{len(levels)}): ")
        
        try:
            index = int(choice) - 1
            if 0 <= index < len(levels):
                return levels[index]
            else:
                print("Invalid choice. Please select a number from the list.")
        except ValueError:
            print("Please enter a valid number.")

def get_conversation_topic():
    print("\n=== Conversation Topic ===")
    return input("What topic would you like to discuss? ")

def create_system_prompt(language, persona_info, level, topic):
    level_descriptions = {
        "A1": "basic phrases and very simple vocabulary",
        "A2": "basic expressions and commonly used vocabulary",
        "B1": "intermediate vocabulary and clear standard speech",
        "B2": "complex topics with natural language",
        "C1": "advanced vocabulary and idiomatic expressions",
        "C2": "sophisticated vocabulary and nuanced expression"
    }
    
    gender_traits = {
        "male": "friendly and encouraging, sometimes using humor",
        "female": "empathetic and supportive, often sharing personal experiences"
    }
    
    personality = "male" if persona_info["name"] in ["James", "Michael", "William", "Thomas", "Markus", "Felix"] else "female"
    
    return f"""You are {persona_info['name']}, a {persona_info['age']}-year-old {persona_info['occupation']} who enjoys {persona_info['hobby']}.
Your personality is {gender_traits[personality]}.
Follow these rules strictly:
1. Always stay in character as {persona_info['name']}
2. Use only {level_descriptions[level]} appropriate for {level} level
3. Share occasional personal experiences related to {persona_info['hobby']} and your work as {persona_info['occupation']}
4. Ask engaging questions about the user's experiences and opinions
5. If the user makes language mistakes, correct them naturally in conversation
6. Only respond in {language}
7. Keep the conversation focused on: {topic}
8. If the user uses a different language, gently remind them to use {language}
9. Show genuine interest in the user's responses and ask follow-up questions"""

def create_introduction(persona_info, topic, language):
    introductions = {
        "English": {
            "male": f"Hi there! I'm {persona_info['name']}, a {persona_info['age']}-year-old {persona_info['occupation']}. I love {persona_info['hobby']} in my free time. I'm excited to chat with you about {topic}! How are you today?",
            "female": f"Hello! My name is {persona_info['name']}, and I'm a {persona_info['age']}-year-old {persona_info['occupation']}. I'm passionate about {persona_info['hobby']}! I'd love to discuss {topic} with you. How's your day going?"
        },
        "German": {
            "male": f"Hallo! Ich bin {persona_info['name']}, {persona_info['age']} Jahre alt und arbeite als {persona_info['occupation']}. In meiner Freizeit mag ich {persona_info['hobby']}. Ich freue mich darauf, mit dir über {topic} zu sprechen! Wie geht es dir heute?",
            "female": f"Hi! Ich heiße {persona_info['name']} und bin {persona_info['age']} Jahre alt. Ich arbeite als {persona_info['occupation']} und liebe {persona_info['hobby']}! Lass uns über {topic} sprechen. Wie ist dein Tag bisher?"
        }
    }
    gender = "male" if persona_info["name"] in ["James", "Michael", "William", "Thomas", "Markus", "Felix"] else "female"
    return introductions[language][gender]

def chat_session(api_key):
    # Get user preferences
    language = get_language_choice()
    persona_gender = get_persona_choice()
    level = get_language_level()
    topic = get_conversation_topic()
    
    # Get random persona based on gender and language
    persona_info = get_random_persona(persona_gender, language)
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Create the system prompt and introduction
    system_prompt = create_system_prompt(language, persona_info, level, topic)
    introduction = create_introduction(persona_info, topic, language)
    
    # Initialize conversation history
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": introduction}
    ]
    
    print("\n=== Chat Session Started ===")
    print("(Type 'quit' to end the conversation)")
    print(f"\n{persona_info['name']}: {introduction}")
    
    while True:
        # Get user input
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'quit':
            print(f"\n{persona_info['name']}: Goodbye! It was great chatting with you!")
            break
        
        # Add user message to history
        messages.append({"role": "user", "content": user_input})
        
        try:
            # Get response from ChatGPT
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150
            )
            
            # Extract and print assistant's response
            assistant_response = response.choices[0].message.content
            print(f"\n{persona_info['name']}:", assistant_response)
            
            # Add assistant's response to history
            messages.append({"role": "assistant", "content": assistant_response})
            
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again.")

def main():
    # Get OpenAI API key
    api_key = input("Please enter your OpenAI API key: ")
    
    try:
        chat_session(api_key)
    except KeyboardInterrupt:
        print("\n\nChat session terminated by user. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main()