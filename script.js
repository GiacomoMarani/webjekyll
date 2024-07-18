async function sendMessage(message) {
    const response = await fetch('http://localhost:8000/chatbot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: message })
    });
    const data = await response.json();
    return data.response;
}

document.getElementById('chat-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    const userInput = document.getElementById('user-input').value;
    const chatBox = document.getElementById('chat-box');

    chatBox.innerHTML += `<div class="chat-message user-message">${userInput}</div>`;

    const botResponse = await sendMessage(userInput);

    chatBox.innerHTML += `<div class="chat-message bot-message">${botResponse}</div>`;
    document.getElementById('user-input').value = '';
});
