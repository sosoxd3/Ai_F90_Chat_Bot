# -*- coding: utf-8 -*-
"""
ai.py
التعامل مع OpenAI للشات
"""

import openai
import config

# تفعيل المفتاح من config
openai.api_key = config.OPENAI_API_KEY

# ==================================
#  دالة أساسية لطلب الرد من GPT
# ==================================
def ask_ai(user_text: str):
    """
    ترسل رسالة إلى نموذج OpenAI وتعيد الرد.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي ترد بالعربية ببساطة ووضوح."},
                {"role": "user", "content": user_text}
            ]
        )

        reply = response.choices[0].message["content"]
        return reply

    except Exception as e:
        return f"⚠️ حدث خطأ أثناء الاتصال بـ OpenAI:\n{str(e)}"
