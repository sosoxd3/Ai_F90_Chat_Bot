# -*- coding: utf-8 -*-
import config
import google.generativeai as genai

# تفعيل مفتاح Google
genai.configure(api_key=config.GOOGLE_API_KEY)

# استخدام موديل Gemini
model = genai.GenerativeModel("gemini-1.5-flash")

def ask_ai(message):
    try:
        response = model.generate_content(message)
        return response.text

    except Exception as e:
        return f"⚠️ حدث خطأ أثناء الاتصال بـ Google AI:\n{str(e)}"
