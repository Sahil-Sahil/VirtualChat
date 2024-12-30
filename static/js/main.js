let currentPersona = null;

async function initializeChat() {
    const language = document.getElementById('language').value;
    const gender = document.getElementById('gender').value;
    const level = document.getElementById('level').value;
    const topic = document.getElementById('topic').value;

    if (!topic) {
        alert('Please enter a conversation topic');
        return;
    }

    try {
        const response = await fetch('/initialize-chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                language,
                gender,
                level,
                topic
            })
        });

        const data = await response.json();

        if (data.success) {
            currentPersona = data.persona;
            
            // Update UI
            document.getElementById('setup-form').style.display = 'none';
            document.getElementById('chat-container').style.display = 'flex';
            
            // Set persona information
            document.getElementById('persona-name').textContent = currentPersona.name;
            document.getElementById('persona-info').textContent = 
                `${currentPersona.age} years old, ${currentPersona.occupation}`;
            
            // Add introduction message
            addMessage(data.introduction, 'assistant');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to initialize chat. Please try again.');
    }
}

async function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();

    if (!message) return;

    // Add user message to chat
    addMessage(message, 'user');
    messageInput.value = '';

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        if (data.success) {
            addMessage(data.response, 'assistant');
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        addMessage('Sorry, there was an error. Please try again.', 'assistant');
    }
}

function addMessage(content, sender) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.textContent = content;
    messagesContainer.appendChild(messageElement);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function endChat() {
    if (confirm('Are you sure you want to end this chat?')) {
        document.getElementById('chat-container').style.display = 'none';
        document.getElementById('setup-form').style.display = 'block';
        // Clear chat messages
        document.getElementById('chat-messages').innerHTML = '';
        // Reset form if needed
        document.getElementById('topic').value = '';
    }
}

// Update the displayPersonaInfo function
function displayPersonaInfo(persona) {
    document.getElementById('persona-name').textContent = persona.name;
    document.getElementById('persona-info').textContent = 
        `${persona.age} years old · ${persona.type} · ${persona.personality}`;
}


// Add enter key listener for message input
document.getElementById('message-input')?.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});