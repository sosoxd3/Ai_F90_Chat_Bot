# -*- coding: utf-8 -*-
"""
main.py
ملف تشغيل بوت Ai F90 Chat Bot
"""

import telebot
from telebot import types
import config
import database as db
import images
import admin_panel
import ai   # الآن ai يعمل مع Google فقط

# ================================
#  تشغيل البوت
# ================================
bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)

# إنشاء قاعدة البيانات عند التشغيل
db.init_db()

# ================================
#  /start
# ================================
@bot.message_handler(commands=["start"])
def start_handler(msg):
    tg_id = msg.from_user.id
    user = db.get_user(tg_id)

    bot.reply_to(msg,
        f"👋 أهلاً بك في {config.BOT_NAME} 🤖\n\n"
        f"💬 رسائل مجانية: {config.FREE_MSG_LIMIT}\n"
        f"🖼️ صور مجانية: {config.FREE_IMG_LIMIT}\n"
        f"💳 للدعم: {config.PAY_TELEGRAM}"
    )

# ================================
#  /admin (تسجيل دخول الادمن)
# ================================
@bot.message_handler(commands=["admin"])
def admin_login(msg):
    chat_id = msg.chat.id
    admin_panel.start_admin_login(bot, chat_id)

# خطوات دخول الادمن
@bot.message_handler(func=lambda m: m.chat.id in admin_panel.login_state)
def admin_login_flow(msg):
    admin_panel.handle_login_flow(bot, msg)

# أوامر الادمن
@bot.message_handler(func=lambda m: m.chat.id in admin_panel.admin_sessions)
def admin_actions(msg):
    admin_panel.handle_admin_actions(bot, msg)

# ================================
#  معالج المستخدم العادي
# ================================
@bot.message_handler(func=lambda m: True)
def user_handler(msg):
    text = msg.text.strip()
    tg_id = msg.from_user.id

    # الحصول على المستخدم
    user = db.get_user(tg_id)
    msgs_used = user[2]
    imgs_used = user[3]
    subscribed = bool(user[4])

    # ========= طلب صورة ==========
    if text.startswith("صورة") or text.startswith("img"):
        if not subscribed and imgs_used >= config.FREE_IMG_LIMIT:
            return bot.reply_to(msg,
                f"❌ انتهى حد الصور المجاني\n"
                f"💰 للدعم: {config.PAY_TELEGRAM}\n"
                f"📞 واتساب: {config.PAY_WHATSAPP}"
            )

        prompt = text.split(" ", 1)[1].strip()
        bot.send_message(msg.chat.id, "⏳ يتم توليد الصورة ...")

        img_bytes, error = images.generate_image(prompt)

        if error:
            return bot.reply_to(msg, error)

        if img_bytes:
            bot.send_chat_action(msg.chat.id, "upload_photo")
            bot.send_photo(msg.chat.id, img_bytes)

            db.update_usage(tg_id, img_inc=1)
            return

    # ========= ذكاء اصطناعي (Google Gemini) ==========
    if not subscribed and msgs_used >= config.FREE_MSG_LIMIT:
        return bot.reply_to(msg,
            f"❌ انتهى حد الرسائل المجاني\n"
            f"💰 للدعم: {config.PAY_TELEGRAM}\n"
            f"📞 واتساب: {config.PAY_WHATSAPP}"
        )

    bot.send_chat_action(msg.chat.id, "typing")
    reply = ai.ask_ai(text)

    bot.reply_to(msg, reply)

    db.update_usage(tg_id, msg_inc=1)

# ================================
#  تشغيل البوت
# ================================
print("✅ Bot is running...")
bot.infinity_polling(skip_pending=True)
