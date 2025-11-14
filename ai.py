# -*- coding: utf-8 -*-
import requests
import config

def ask_ai(message):
    if not config.GOOGLE_API_KEY:
        return "❌ GOOGLE_API_KEY غير موجود!"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={config.GOOGLE_API_KEY}"

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

        if "error" in data:
            return f"⚠️ خطأ من Google AI:\n{data}"

        reply = data["candidates"][0]["content"]["parts"][0]["text"]
        return reply

    except Exception as e:
        return f"⚠️ حدث خطأ أثناء الاتصال بـ Google AI:\n{str(e)}"
