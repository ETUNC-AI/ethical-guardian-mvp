document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');

    const sendMessage = async () => {
        const userText = messageInput.value.trim();
        if (userText === '') return;

        appendMessage(userText, 'user-message');
        messageInput.value = '';
        const typingIndicator = appendMessage('Guardian is thinking...', 'guardian-message');

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: userText })
            });
            const data = await response.json();

            chatBox.removeChild(typingIndicator);
            appendMessage(data.guardian_output, 'guardian-message');

        } catch (error) {
            chatBox.removeChild(typingIndicator);
            appendMessage('Error: Could not connect to the Guardian.', 'guardian-message');
        }
    };

    const appendMessage = (text, className) => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', className);
        const p = document.createElement('p');
        p.textContent = text;
        messageDiv.appendChild(p);
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
        return messageDiv;
    };

    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendMessage();
        }
    });
});
