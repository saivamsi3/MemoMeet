document.addEventListener('DOMContentLoaded', function() {
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');
    const chatMessages = document.getElementById('chatMessages');

    function addMessage(content, isUser) {
        const div = document.createElement('div');
        div.className = `chat-message ${isUser ? 'user' : 'bot'} mb-3 p-3 rounded`;
        div.textContent = content;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async function sendMessage() {
        const question = chatInput.value.trim();
        if (!question) return;

        addMessage(question, true);
        chatInput.value = '';

        addMessage('Thinking...', false);

        try {
            const res = await fetch('/chat/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({question: question})
            });
            const data = await res.json();
            chatMessages.lastChild.textContent = data.answer;
        } catch (err) {
            chatMessages.lastChild.textContent = 'Sorry, something went wrong.';
        }
    }

    if (sendBtn) {
        sendBtn.addEventListener('click', sendMessage);
    }
    if (chatInput) {
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    }

    document.querySelectorAll('.sample-q').forEach(btn => {
        btn.addEventListener('click', function() {
            chatInput.value = this.textContent.trim();
            sendMessage();
        });
    });
});
