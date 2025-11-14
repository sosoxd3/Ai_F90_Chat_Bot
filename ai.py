# -*- coding: utf-8 -*-
"""
ai.py
معالجة الدردشة باستخدام Google AI Studio
"""

import requests
import config


def ask_ai(message: str):
    """
    إرسال رسالة إلى Google Gemini والحصول على الرد.
    """

    if not config.GOOGLE_API_KEY:
        return "❌ GOOGLE_API_KEY غير موجود في Render."

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

        if response.status_code != 200:
            return f"⚠️ خطأ من Google AI:\n{response.text}"

        data = response.json()

        # مسار النص في استجابة Google
        try:
            reply = data["candidates"][0]["content"]["parts"][0]["text"]
            return reply
        except:
            return "⚠️ لم يتم استلام رد مفهوم من Google."

    except Exception as e:
        return f"⚠️ حدث خطأ أثناء الاتصال بـ Google AI:\n{str(e)}"
