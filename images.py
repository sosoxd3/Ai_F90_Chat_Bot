# -*- coding: utf-8 -*-
"""
images.py
توليد الصور باستخدام Google AI Studio
"""

import requests
import base64
import config


# ================================
#   دالة توليد صورة
# ================================
def generate_image(prompt: str):
    """
    ترسل طلب توليد صورة إلى Google AI وتعيد Bytes جاهزة للإرسال.
    """

    if not config.GOOGLE_API_KEY:
        return None, "❌ GOOGLE_API_KEY غير موجود في Render."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagegeneration:generateImage?key={config.GOOGLE_API_KEY}"

    payload = {
        "prompt": {
            "text": prompt
        }
    }

    try:
        response = requests.post(url, json=payload, timeout=50)

        if response.status_code != 200:
            return None, f"⚠️ خطأ من Google AI: {response.text}"

        data = response.json()

        # استجابة جوجل تختلف حساب كل حساب — نعالج الاثنين
        images = data.get("images") or data.get("candidates")

        if not images:
            return None, "⚠️ لم يتم العثور على أي صورة في الرد."

        # بعضها يكون تحت key اسمه 'base64'
        img_b64 = images[0].get("base64") if isinstance(images[0], dict) else None

        if not img_b64:
            return None, "⚠️ لم يتم العثور على بيانات الصورة Base64."

        img_bytes = base64.b64decode(img_b64)

        return img_bytes, None

    except Exception as e:
        return None, f"⚠️ حدث خطأ أثناء الاتصال بـ Google AI:\n{str(e)}"
