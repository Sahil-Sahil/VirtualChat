from openai import OpenAI

class ChatSession:
    def __init__(self, api_key, language, persona, level, topic):
        self.client = OpenAI(api_key=api_key)
        self.language = language
        self.persona = persona
        self.level = level
        self.topic = topic
        self.messages = []
        self._initialize_chat()

    def _initialize_chat(self):
        system_prompt = self._create_system_prompt()
        introduction = self._create_introduction()
        
        self.messages = [
            {"role": "system", "content": system_prompt},
            {"role": "assistant", "content": introduction}
        ]
        
        return introduction

    def _create_system_prompt(self):
        level_descriptions = {
            "A1": "basic phrases and very simple vocabulary",
            "A2": "basic expressions and commonly used vocabulary",
            "B1": "intermediate vocabulary and clear standard speech",
            "B2": "complex topics with natural language",
            "C1": "advanced vocabulary and idiomatic expressions",
            "C2": "sophisticated vocabulary and nuanced expression"
        }
        
        gender = "male" if self.persona["gender"] == "male" else "female"
        gender_traits = {
            "male": "friendly and encouraging, sometimes using humor",
            "female": "empathetic and supportive, often sharing personal experiences"
        }
        
        return f"""You are {self.persona['name']}, a {self.persona['age']}-year-old {self.persona['occupation']} who enjoys {self.persona['hobby']}.
Your personality is {gender_traits[gender]}.
Follow these rules strictly:
1. Always stay in character as {self.persona['name']}
2. Use only {level_descriptions[self.level]} appropriate for {self.level} level
3. Share occasional personal experiences related to {self.persona['hobby']} and your work
4. Ask engaging questions about the user's experiences and opinions
5. If the user makes language mistakes, correct them naturally in conversation
6. Only respond in {self.language}
7. Keep the conversation focused on: {self.topic}
8. If the user uses a different language, gently remind them to use {self.language}
9. Show genuine interest in the user's responses and ask follow-up questions"""

    def _create_introduction(self):
        introductions = {
            "English": {
                "male": f"Hi there! I'm {self.persona['name']}, a {self.persona['age']}-year-old {self.persona['occupation']}. I love {self.persona['hobby']} in my free time. I'm excited to chat with you about {self.topic}! How are you today?",
                "female": f"Hello! My name is {self.persona['name']}, and I'm a {self.persona['age']}-year-old {self.persona['occupation']}. I'm passionate about {self.persona['hobby']}! I'd love to discuss {self.topic} with you. How's your day going?"
            },
            "German": {
                "male": f"Hallo! Ich bin {self.persona['name']}, {self.persona['age']} Jahre alt und arbeite als {self.persona['occupation']}. In meiner Freizeit mag ich {self.persona['hobby']}. Ich freue mich darauf, mit dir über {self.topic} zu sprechen! Wie geht es dir heute?",
                "female": f"Hi! Ich heiße {self.persona['name']} und bin {self.persona['age']} Jahre alt. Ich arbeite als {self.persona['occupation']} und liebe {self.persona['hobby']}! Lass uns über {self.topic} sprechen. Wie ist dein Tag bisher?"
            }
        }
        return introductions[self.language][self.persona["gender"]]

    def send_message(self, message):
        self.messages.append({"role": "user", "content": message})
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            max_tokens=150
        )
        
        assistant_response = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": assistant_response})
        
        return assistant_response

def create_chat_session(api_key, language, persona, level, topic):
    return ChatSession(api_key, language, persona, level, topic)