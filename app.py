from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os # 1. os 라이브러리를 불러옵니다.

# --- 설정 부분 ---
# 2. Render의 환경 변수에서 'GEMINI_API_KEY'라는 이름의 키를 가져옵니다.
API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"

# --- Flask 앱 설정 ---
app = Flask(__name__)
CORS(app)

# 대화 기록을 서버 메모리에 저장 (간단한 방식)
chat_history = []

@app.route('/chat', methods=['POST'])
def handle_chat():
    global chat_history
    user_message = request.json['message']
    print(f"프론트엔드로부터 받은 메시지: {user_message}")

    # API 키가 설정되지 않았을 경우 오류 메시지 반환
    if not API_KEY:
        error_msg = "오류: 서버에 API 키가 설정되지 않았습니다. Render 환경 변수를 확인해주세요."
        print(error_msg)
        return jsonify({'response': error_msg})

    chat_history.append({"role": "user", "parts": [{"text": user_message}]})

    payload = {
        "contents": chat_history,
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    }

    try:
        response = requests.post(GEMINI_API_URL, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
        response.raise_for_status()

        data = response.json()
        
        if 'candidates' in data and data['candidates']:
            bot_response = data['candidates'][0]['content']['parts'][0]['text']
        else:
            bot_response = "죄송합니다, 답변을 받지 못했습니다."
            if chat_history and chat_history[-1]['role'] == 'user':
                chat_history.pop()

        chat_history.append({"role": "model", "parts": [{"text": bot_response}]})

    except Exception as e:
        print(f"API 호출 오류: {e}")
        if chat_history and chat_history[-1]['role'] == 'user':
            chat_history.pop()
        bot_response = "죄송합니다, 답변을 생성하는 중 오류가 발생했습니다. API 키나 서버 상태를 확인해주세요."

    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)