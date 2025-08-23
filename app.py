from flask import Flask, request, jsonify
from flask_cors import CORS
import requests  # google-generativeai 대신 requests를 직접 사용
import json

# --- 설정 부분 ---
API_KEY = "AIzaSyDO2lqz5CfSSXCjPfOK8GCz3HOpgj0KRCU"
# Gemini API의 공식 주소(Endpoint)
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

    # 대화 기록에 사용자 메시지 추가
    chat_history.append({"role": "user", "parts": [{"text": user_message}]})

    # Gemini API에 보낼 데이터 형식
    payload = {
        "contents": chat_history,
        "safetySettings": [ # 안전 설정을 API가 요구하는 정확한 형식으로 전달
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    }

    try:
        # requests 라이브러리를 사용해 Gemini API에 직접 POST 요청
        response = requests.post(GEMINI_API_URL, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
        response.raise_for_status() # 오류가 있으면 예외 발생

        data = response.json()
        
        # API 응답에서 텍스트 추출
        bot_response = data['candidates'][0]['content']['parts'][0]['text']
        
        # 대화 기록에 Gemini 응답 추가
        chat_history.append({"role": "model", "parts": [{"text": bot_response}]})

    except Exception as e:
        print(f"API 호출 오류: {e}")
        # 오류 발생 시 대화 기록에서 마지막 사용자 메시지 제거
        if chat_history and chat_history[-1]['role'] == 'user':
            chat_history.pop()
        bot_response = "죄송합니다, 답변을 생성하는 중 오류가 발생했습니다. API 키나 서버 상태를 확인해주세요."

    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)