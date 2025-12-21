document.addEventListener('DOMContentLoaded', function() {
    const chatIcon = document.getElementById('chat-icon');
    const chatWindow = document.getElementById('chat-window');
    const closeChat = document.getElementById('close-chat');
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    // Toggle chat window visibility
    chatIcon.addEventListener('click', () => {
        chatWindow.classList.remove('hidden');
        // Add welcome message if there are no messages
        if (chatMessages.children.length === 0) {
            addBotMessage("Welcome back Frosty! How can I help you today?");
        }
        userInput.focus();
    });

    closeChat.addEventListener('click', () => {
        chatWindow.classList.add('hidden');
    });

    // Handle sending messages
    function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;
        
        // Add user message to chat
        addUserMessage(message);
        userInput.value = '';
        
        // Create a placeholder for the bot's response
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'Frosty bot-message typing';
        typingIndicator.textContent = 'Typing...';
        chatMessages.appendChild(typingIndicator);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Send request to the server
        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: message })
        })
        .then(response => {
            const reader = response.body.getReader();
            let responseText = '';
            
            // Remove typing indicator
            chatMessages.removeChild(typingIndicator);
            
            // Create bot message element
            const botMessageElement = document.createElement('div');
            botMessageElement.className = 'message bot-message';
            chatMessages.appendChild(botMessageElement);
            
            function readStream() {
                return reader.read().then(({ done, value }) => {
                    if (done) {
                        return;
                    }
                    
                    // Convert the chunk to text and append it
                    const chunk = new TextDecoder().decode(value);
                    responseText += chunk;
                    botMessageElement.textContent = responseText;
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                    
                    return readStream();
                });
            }
            
            return readStream();
        })
        .catch(error => {
            // Remove typing indicator if there's an error
            if (typingIndicator.parentNode === chatMessages) {
                chatMessages.removeChild(typingIndicator);
            }
            
            addBotMessage("Sorry, I encountered an error while processing your request.");
            console.error('Error:', error);
        });
    }

    function addUserMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message';
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function addBotMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});