# -*- coding: utf-8 -*-
import openai
import config

# تعيين المفتاح
openai.api_key = config.OPENAI_API_KEY

def ask_openai(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي."},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message["content"]

    except Exception as e:
        return f"⚠️ حدث خطأ أثناء الاتصال بـ OpenAI:\n{str(e)}"
