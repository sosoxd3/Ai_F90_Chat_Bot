here# -*- coding: utf-8 -*-

# ========== إعدادات عامة ==========
BOT_NAME = "Ai F90 Chat Bot"

# حدود الاستخدام المجاني
FREE_MSG_LIMIT = 20      # الرسائل
FREE_IMG_LIMIT = 5       # الصور

# معلومات الدفع / الاشتراك
PAY_TELEGRAM = "@F90xd"
PAY_WHATSAPP = "https://wa.me/962792681340"

# معلومات الإدمن
ADMINS = {
    "f90": "9163",
    "fahad": "1122",
}

# ========== مفاتيح API ==========
# ⚠️ لا تكتب المفاتيح هنا أبداً
# Render سيضعها بشكل آمن عبر Environment Variables

import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY     = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY     = os.getenv("GOOGLE_API_KEY")

# تأكد أن المفاتيح موجودة
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN غير موجود في Environment!")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY غير موجود في Environment!")
if not GOOGLE_API_KEY:
    print("⚠️ GOOGLE_API_KEY غير مضاف — ميزة الصور قد لا تعمل.")
