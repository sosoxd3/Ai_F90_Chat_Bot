# -*- coding: utf-8 -*-
import requests
import config

def ask_ai(message):
    if not config.GOOGLE_API_KEY:
        return "❌ GOOGLE_API_KEY غير موجود!"

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={config.GOOGLE_API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": message}
                ]
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, timeout=50)
        data = response.json()

        # إذا Google رجع خطأ
        if "error" in data:
            return f"⚠️ خطأ من Google:\n{data['error']['message']}"

        # استخراج الرد النصي
        reply = data["candidates"][0]["content"]["parts"][0]["text"]
        return reply

    except Exception as e:
        return f"⚠️ حدث خطأ:\n{str(e)}"
