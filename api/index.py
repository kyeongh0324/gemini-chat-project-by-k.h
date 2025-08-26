from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, json, os

API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-1.5-flash-latest:generateContent?key=" + (API_KEY or "")
)

app = Flask(__name__)
CORS(app)

# ✅ 건강 체크 (GET)
@app.route('/health', methods=['GET'])
@app.route('/api/index/health', methods=['GET'])   # Vercel이 풀 경로로 넘기는 경우 대비
def health():
    return jsonify({'ok': True})

# ✅ 실제 처리 라우트: 루트, 풀경로, 그리고 catch-all 모두 허용
@app.route('/', methods=['POST'])
@app.route('/api/index', methods=['POST'])         # 정확 경로 매칭
@app.route('/<path:subpath>', methods=['POST'])    # catch-all (ex: /api/index, /api, 기타)
def handle_chat(subpath=''):
    data = request.get_json(silent=True) or {}
    user_message = (data.get('message') or '').strip()

    if not user_message:
        return jsonify({'response': '메시지가 비어 있습니다.'}), 400

    if not API_KEY:
        return jsonify({'response': '서버에 API 키가 설정되지 않았습니다.'}), 500

    payload = {
        "contents": [{"role": "user", "parts": [{"text": user_message}]}],
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    }
    try:
        r = requests.post(
            GEMINI_API_URL,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(payload),
            timeout=30
        )
        r.raise_for_status()
        data = r.json()
        bot_response = data['candidates'][0]['content']['parts'][0]['text']
        return jsonify({'response': bot_response})
    except Exception as e:
        print(f"[server] Gemini API 호출 오류: {e}")
        return jsonify({'response': '죄송합니다, 답변 생성 중 오류가 발생했습니다.'}), 502
