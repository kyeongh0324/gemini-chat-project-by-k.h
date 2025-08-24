# 파일: api/index.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, json, os

API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def handle_chat():
    user_message = request.json['message']
    chat_history = [{"role": "user", "parts": [{"text": user_message}]}]

    if not API_KEY:
        return jsonify({'response': "서버에 API 키가 설정되지 않았습니다."})

    # (이하 Gemini API 호출 로직은 그대로 유지)
    payload = {"contents": chat_history, "safetySettings": [{"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},{"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},{"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},{"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}]}
    try:
        response = requests.post(GEMINI_API_URL, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        bot_response = data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"API 호출 오류: {e}")
        bot_response = "죄송합니다, 답변 생성 중 오류가 발생했습니다."
    return jsonify({'response': bot_response})