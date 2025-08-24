# 파일 이름: api/index.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os

# API 키를 환경 변수에서 가져옵니다.
API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"

# Vercel이 인식할 수 있도록 app 변수 이름을 handler로 사용하기도 합니다.
# Flask 앱 생성
app = Flask(__name__)
CORS(app)

# 대화 기록은 이제 요청마다 새로 관리해야 합니다. (서버리스 특성)
# 더 복잡한 앱에서는 데이터베이스를 사용합니다.

@app.route('/chat', methods=['POST'])
def handle_chat():
    user_message = request.json['message']
    # 서버리스 환경에서는 이전 대화 기록을 프론트엔드에서 받아야 합니다.
    # 지금은 간단하게 매번 새로운 대화를 시작하도록 구현합니다.
    chat_history = [{"role": "user", "parts": [{"text": user_message}]}]

    if not API_KEY:
        return jsonify({'response': "서버에 API 키가 설정되지 않았습니다."})

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
        bot_response = data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"API 호출 오류: {e}")
        bot_response = "죄송합니다, 답변 생성 중 오류가 발생했습니다."

    return jsonify({'response': bot_response})