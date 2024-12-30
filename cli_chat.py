import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize the client
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url="https://api.openai.com/v1"
)

def get_language_choice():
    while True:
        print("\n=== Language Selection ===")
        print("1. English")
        print("2. German")
        choice = input("Please select your target language (1/2): ")
        return "English" if choice == "1" else "German"

def get_persona_choice():
    while True:
        print("\n=== Chat Partner Persona ===")
        print("1. Male")
        print("2. Female")
        choice = input("Please select your chat partner's gender (1/2): ")
        return "male" if choice == "1" else "female"

def get_language_level():
    print("\n=== Language Level ===")
    print("1. A1 - Beginner")
    print("2. A2 - Elementary")
    print("3. B1 - Intermediate")
    print("4. B2 - Upper Intermediate")
    print("5. C1 - Advanced")
    print("6. C2 - Mastery")
    choice = input("Select your level (1-6): ")
    levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
    return levels[int(choice) - 1]

def chat_with_ai(messages):
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"\nError: {str(e)}")
        return None

def main():
    # Get user preferences
    language = get_language_choice()
    persona = get_persona_choice()
    level = get_language_level()
    
    print("\n=== Conversation Topic ===")
    topic = input("What would you like to talk about? ")

    # Create system prompt
    system_prompt = f"You are a {persona} native {language} speaker. Use language appropriate for {level} level. Let's discuss {topic}."
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": f"Hello! I'd love to chat with you about {topic} in {language}. How are you today?"}
    ]

    print("\n=== Chat Started ===")
    print("Assistant: Hello! I'd love to chat with you about " + topic + ". How are you today?")
    print("(Type 'quit' to end the chat)")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            print("\nGoodbye!")
            break

        messages.append({"role": "user", "content": user_input})
        
        response = chat_with_ai(messages)
        if response:
            print("\nAssistant:", response)
            messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()