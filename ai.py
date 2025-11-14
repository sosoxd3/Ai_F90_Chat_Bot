# -*- coding: utf-8 -*-
"""
ai.py
التعامل مع OpenAI (الإصدار الجديد)
"""

from openai import OpenAI
import config

client = OpenAI(api_key=config.OPENAI_API_KEY)

def ask_ai(text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي ترد بالعربية."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message["content"]

    except Exception as e:
        return f"⚠️ حدث خطأ أثناء الاتصال بـ OpenAI:\n{e}"
