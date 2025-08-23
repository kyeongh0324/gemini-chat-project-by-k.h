// HTML 요소들을 가져옵니다.
const sendButton = document.getElementById('sendButton');
const userInput = document.getElementById('userInput');
const chatWindow = document.querySelector('.chat-window');

sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

async function sendMessage() {
    const message = userInput.value;
    if (message.trim() === '') return;

    addMessage('나', message);
    userInput.value = '';

    try {
        // ⬇️ 백엔드 서버의 전체 주소를 정확하게 입력합니다 ⬇️
        const response = await fetch('http://127.0.0.1:5000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });

        // ⬆️ 여기가 수정된 부분입니다 ⬆️

        if (!response.ok) {
            // 서버 응답이 200번대가 아닐 경우 (예: 404, 500 오류)
            throw new Error(`서버 오류: ${response.status}`);
        }

        const data = await response.json();
        addMessage('Gemini', data.response);

    } catch (error) {
        console.error('오류:', error);
        addMessage('오류', '서버와 통신 중 문제가 발생했습니다. 백엔드 서버가 켜져 있는지, 주소가 올바른지 확인하세요.');
    }
}

function addMessage(sender, message) {
    const messageElement = document.createElement('p');
    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
    if (sender === '나') {
        messageElement.style.textAlign = 'right';
        messageElement.style.color = 'blue';
    }
    chatWindow.appendChild(messageElement);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}