# 파일: api/index.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, json, os

API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"

app = Flask(__name__)
CORS(app)

# Vercel이 어떤 경로로 요청을 보내든 모두 이 함수가 처리하도록 설정
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def handle_chat(path):
    # 실제 채팅 로직은 POST 요청일 때만 실행
    if request.method == 'POST':
        try:
            user_message = request.json['message']
            print(f"[서버 로그] 받은 메시지: {user_message}") # 로그 추가
        except:
            return jsonify({'response': '메시지 형식이 올바르지 않습니다.'}), 400

        if not API_KEY:
            print("[서버 로그] 오류: API 키가 설정되지 않았습니다.")
            return jsonify({'response': '서버에 API 키가 설정되지 않았습니다.'}), 500

        chat_history = [{"role": "user", "parts": [{"text": user_message}]}]
        payload = {"contents": chat_history, "safetySettings": [{"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},{"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},{"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},{"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}]}
        
        try:
            response = requests.post(GEMINI_API_URL, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=30)
            response.raise_for_status()
            data = response.json()
            bot_response = data['candidates'][0]['content']['parts'][0]['text']
            return jsonify({'response': bot_response})
        except Exception as e:
            print(f"[서버 로그] Gemini API 호출 오류: {e}")
            return jsonify({'response': '죄송합니다, 답변 생성 중 서버 내부 오류가 발생했습니다.'}), 500
    
    # POST 요청이 아닐 경우 (예: 브라우저로 직접 접속 시도)
    return "이 주소는 챗봇 API 엔드포인트입니다."