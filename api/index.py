# 파일: api/index.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, json, os

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def handle_chat():
    print("[서버 로그] 함수가 호출되었습니다.") # 실행 여부 확인용 로그
    try:
        API_KEY = os.environ.get('GEMINI_API_KEY')
        if not API_KEY:
            print("[서버 로그] 오류: API 키가 설정되지 않았습니다.")
            return jsonify({'response': "서버에 API 키가 설정되지 않았습니다."}), 500

        GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"
        
        user_message = request.json['message']
        print(f"[서버 로그] 받은 메시지: {user_message}")

        chat_history = [{"role": "user", "parts": [{"text": user_message}]}]
        payload = {"contents": chat_history, "safetySettings": [{"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},{"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},{"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},{"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}]}
        
        response = requests.post(GEMINI_API_URL, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=30)
        response.raise_for_status()
        data = response.json()
        bot_response = data['candidates'][0]['content']['parts'][0]['text']
        
        print("[서버 로그] 성공적으로 답변을 생성했습니다.")
        return jsonify({'response': bot_response})

    except Exception as e:
        print(f"[서버 로그] 심각한 오류 발생: {e}")
        return jsonify({'response': '죄송합니다, 서버 내부에서 심각한 오류가 발생했습니다.'}), 500