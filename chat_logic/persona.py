import random

def generate_vtuber_name(gender):
    # Simple name generation
    prefixes = ["Sky", "Star", "Moon", "Crystal", "Pixel", "Neo", "Cyber", "Virtual"]
    female_suffixes = ["Luna", "Rose", "Heart", "Bell", "Song", "Light", "Wave", "Spirit"]
    male_suffixes = ["Knight", "Blade", "Storm", "Byte", "Spark", "Pulse", "Stream", "Code"]
    
    prefix = random.choice(prefixes)
    suffix = random.choice(female_suffixes if gender == "female" else male_suffixes)
    return f"{prefix}{suffix}"

def generate_vtuber_traits(gender):
    personalities = [
        "energetic and cheerful",
        "calm and soothing",
        "quirky and creative",
        "intellectual and curious",
        "playful and mischievous",
        "friendly and supportive"
    ]
    
    hobbies = [
        "gaming",
        "singing",
        "digital art",
        "storytelling",
        "music composition",
        "anime watching",
        "cosplay designing",
        "virtual world exploring"
    ]
    
    return {
        "personality": random.choice(personalities),
        "hobby": random.choice(hobbies)
    }

def get_random_persona(gender, language):
    traits = generate_vtuber_traits(gender)
    return {
        "name": generate_vtuber_name(gender),
        "gender": gender,
        "personality": traits["personality"],
        "hobby": traits["hobby"],
        "type": "VTuber",
        "occupation": "Virtual Content Creator",
        "age": random.randint(18, 25)  # Common VTuber age range
    }

def get_introduction_by_language(language, persona, topic, level):
    introductions = {
        "English": {
            "A1": f"Hi! I'm {persona['name']}! I like {persona['hobby']}. Let's talk about {topic}!",
            "A2": f"Hello! I'm {persona['name']}, and I enjoy {persona['hobby']}. I'd love to talk about {topic} with you!",
            "B1": f"Hi there! I'm {persona['name']}, and I'm passionate about {persona['hobby']}. Let's have a chat about {topic}!",
            "B2": f"Hey! I'm {persona['name']}, and I'm really into {persona['hobby']}. I'm excited to discuss {topic} with you!",
            "C1": f"Greetings! I'm {persona['name']}, and I'm absolutely passionate about {persona['hobby']}. I'm looking forward to having an engaging discussion about {topic}!",
            "C2": f"Delighted to meet you! I'm {persona['name']}, and I'm thoroughly enthusiastic about {persona['hobby']}. I'm eagerly anticipating our discussion about {topic}!"
        },
        "German": {
            "A1": f"Hallo! Ich bin {persona['name']}! Ich mag {persona['hobby']}. Lass uns über {topic} sprechen!",
            "A2": f"Hallo! Ich heiße {persona['name']} und ich mag {persona['hobby']}. Lass uns über {topic} reden!",
            "B1": f"Hallo zusammen! Ich bin {persona['name']} und ich interessiere mich für {persona['hobby']}. Lass uns über {topic} sprechen!",
            "B2": f"Hey! Ich bin {persona['name']} und ich begeistere mich für {persona['hobby']}. Ich freue mich darauf, mit dir über {topic} zu diskutieren!",
            "C1": f"Grüß dich! Ich bin {persona['name']} und ich bin total begeistert von {persona['hobby']}. Ich freue mich sehr auf unser Gespräch über {topic}!",
            "C2": f"Herzlich willkommen! Ich bin {persona['name']} und ich bin außerordentlich fasziniert von {persona['hobby']}. Ich bin sehr gespannt auf unseren Austausch über {topic}!"
        }
    }
    return introductions[language][level]

def get_level_guidelines(level):
    return {
        "A1": {
            "vocabulary": "Use only basic words and phrases. Stick to present tense. Use simple sentences.",
            "grammar": "Use only basic present tense. Avoid complex sentences. Use mainly subject + verb + object structure.",
            "topics": "Focus on immediate environment, basic personal information, and simple daily activities.",
            "examples": {
                "English": ["I am", "I like", "I want", "This is", "That is"],
                "German": ["Ich bin", "Ich mag", "Ich möchte", "Das ist", "Hier ist"]
            }
        },
        "A2": {
            "vocabulary": "Use basic but slightly more varied vocabulary. Introduce simple past tense.",
            "grammar": "Use simple present and past tense. Introduce basic conjunctions (and, but, because).",
            "topics": "Daily routines, simple experiences, basic needs, simple opinions.",
            "examples": {
                "English": ["I went", "I would like", "because", "sometimes", "usually"],
                "German": ["Ich war", "Ich möchte", "weil", "manchmal", "normalerweise"]
            }
        },
        "B1": {
            "vocabulary": "Use intermediate vocabulary. Include some idiomatic expressions.",
            "grammar": "Use various tenses. Introduce conditional sentences.",
            "topics": "Personal experiences, hopes, dreams, brief explanations of opinions and plans.",
            "examples": {
                "English": ["I would have", "If I could", "In my opinion", "I believe that"],
                "German": ["Ich hätte", "Wenn ich könnte", "Meiner Meinung nach", "Ich glaube, dass"]
            }
        },
        "B2": {
            "vocabulary": "Use varied vocabulary. Include common idiomatic expressions.",
            "grammar": "Use complex sentence structures. All tenses allowed.",
            "topics": "Current events, abstract topics, detailed explanations.",
            "examples": {
                "English": ["Nevertheless", "Moreover", "In contrast", "Subsequently"],
                "German": ["Dennoch", "Außerdem", "Im Gegensatz dazu", "Anschließend"]
            }
        },
        "C1": {
            "vocabulary": "Use sophisticated vocabulary. Include advanced idiomatic expressions.",
            "grammar": "Use all grammatical structures. Complex and compound sentences.",
            "topics": "Complex academic topics, hypothetical situations, nuanced opinions.",
            "examples": {
                "English": ["Consequently", "Furthermore", "Notwithstanding", "In light of"],
                "German": ["Folglich", "Darüber hinaus", "Trotzdem", "Angesichts"]
            }
        },
        "C2": {
            "vocabulary": "Use highly sophisticated vocabulary. Include rare words and expressions.",
            "grammar": "Use all grammatical structures with complete accuracy.",
            "topics": "Any topic with complete fluency and accuracy.",
            "examples": {
                "English": ["Albeit", "Hereinafter", "Whilst", "Whereupon"],
                "German": ["Wenngleich", "Hiernach", "Währenddessen", "Woraufhin"]
            }
        }
    }[level]