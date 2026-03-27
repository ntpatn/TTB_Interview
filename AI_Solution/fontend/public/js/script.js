const btnSend = document.getElementById('btn-send');
const msgInput = document.getElementById('msg-input');
const chatBox = document.getElementById('chat-box');

// const API_ENDPOINT = 'http://localhost:8008/chat/conversation';  
const API_ENDPOINT = 'http://localhost:8008/chat/conversation/auto'

let conversationHistory = [];

async function sendMessage() {
    const text = msgInput.value.trim();
    if (!text) return;
    chatBox.innerHTML += `
        <div class="d-flex justify-content-end mb-2">
            <div class="bg-primary text-white p-2 rounded"><strong>You</strong>: ${text}</div>
        </div>`;
    msgInput.value = '';
    chatBox.scrollTop = chatBox.scrollHeight;
    try {

        const response = await fetch(API_ENDPOINT, { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                message: text,
                user_id: "guest",
                conversation_history: conversationHistory
            }) 
        });

        const data = await response.json();
        const aiText = data.reply || JSON.stringify(data); 

        chatBox.innerHTML += `
            <div class="d-flex justify-content-start mb-2">
                <div class="bg-light border p-2 rounded text-dark"><strong>AI:</strong> ${aiText}</div>
            </div>`;

        conversationHistory.push({
            role: "user",
            content: text
        });
        conversationHistory.push({
            role: "assistant",
            content: aiText
        });
        
        if (conversationHistory.length > 10) {
            conversationHistory = conversationHistory.slice(-10);
        }

    } catch (error) {
        chatBox.innerHTML += `<div class="text-danger text-center">Error: ${error.message}</div>`;
    }
    chatBox.scrollTop = chatBox.scrollHeight;
}

btnSend.onclick = sendMessage;

msgInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});