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
        const response = await fetch('http://kyeongh0324.pythonanywhere.com/chat', {
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
    const messageContainer = document.querySelector('.message-container');
    const messageDiv = document.createElement('div');

    // ⬇️ 여기가 수정된 부분입니다 ⬇️
    let displayName = sender; // 표시될 이름을 저장할 변수

    if (sender === '나') {
        messageDiv.className = 'message user-message';
    } else { // '나'가 아닌 경우 (Gemini, 오류 등)
        messageDiv.className = 'message bot-message';
        // 실제 발신자(sender)가 'Gemini'일 때만 표시 이름을 '경환'으로 변경
        if (sender === 'Gemini') {
            displayName = '경환i';
        }
    }
    // ⬆️ 여기까지 수정되었습니다 ⬆️

    // innerHTML 대신 innerText를 사용하고, strong 태그로 이름을 감싸줍니다.
    const strongElement = document.createElement('strong');
    strongElement.innerText = `${displayName}: `;
    
    messageDiv.appendChild(strongElement);
    messageDiv.append(message); // append를 사용해 텍스트를 추가합니다.

    messageContainer.appendChild(messageDiv);

    const chatWindow = document.querySelector('.chat-window');
    chatWindow.scrollTop = chatWindow.scrollHeight;
}