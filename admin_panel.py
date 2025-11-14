# -*- coding: utf-8 -*-
"""
admin_panel.py
نظام الإدارة والتحكم في بوت Ai F90 Chat Bot
"""

import telebot
from telebot import types

import config
import database as db


# جلسات الإدمن (الذين قاموا بتسجيل الدخول)
admin_sessions = set()

# حالات تسجيل الدخول
login_state = {}   # {chat_id: {"step": "username" / "password", "username": "..."}}


# ============================
#   بدء تسجيل دخول الإدمن
# ============================
def start_admin_login(bot, chat_id):
    login_state[chat_id] = {"step": "username"}
    bot.send_message(chat_id, "🔐 أدخل اسم المستخدم للإدمن:")


# ============================
#  معالجة خطوات تسجيل الدخول
# ============================
def handle_login_flow(bot, message):
    chat_id = message.chat.id
    text = message.text.strip()

    if chat_id not in login_state:
        return

    step = login_state[chat_id]["step"]

    # 1) username
    if step == "username":
        login_state[chat_id]["username"] = text
        login_state[chat_id]["step"] = "password"
        bot.send_message(chat_id, "🔑 أدخل كلمة المرور:")
        return

    # 2) password
    if step == "password":
        username = login_state[chat_id]["username"]
        password = text

        if username in config.ADMINS and config.ADMINS[username] == password:
            admin_sessions.add(chat_id)
            login_state.pop(chat_id, None)
            show_admin_menu(bot, chat_id)
        else:
            bot.send_message(chat_id, "❌ اسم المستخدم أو كلمة المرور غير صحيحة.")
            login_state.pop(chat_id, None)


# ============================
#   قائمة لوحة التحكم
# ============================
def show_admin_menu(bot, chat_id):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    kb.row("📊 الإحصائيات")
    kb.row("👤 فحص مستخدم")
    kb.row("⭐ تفعيل اشتراك", "❌ إلغاء اشتراك")
    kb.row("📢 رسالة جماعية")
    kb.row("🔓 تسجيل خروج")

    bot.send_message(chat_id, "✅ تم تسجيل الدخول إلى لوحة تحكم الإدمن.\nاختر من القائمة:", reply_markup=kb)


# ============================
#   معالجة ضغطات الإدمن
# ============================
def handle_admin_actions(bot, message):
    chat_id = message.chat.id
    text = message.text.strip()

    # إذا خرج من النظام
    if text == "🔓 تسجيل خروج":
        admin_sessions.discard(chat_id)
        bot.send_message(chat_id, "✔️ تم تسجيل الخروج.", reply_markup=types.ReplyKeyboardRemove())
        return

    # الإحصائيات العامة
    if text == "📊 الإحصائيات":
        conn = db.sqlite3.connect(db.DB_NAME)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM users")
        total = c.fetchone()[0]
        conn.close()

        bot.send_message(chat_id, f"📊 عدد المستخدمين المسجلين: {total}")
        return

    # فحص مستخدم
    if text == "👤 فحص مستخدم":
        login_state[chat_id] = {"step": "check_user"}
        bot.send_message(chat_id, "أرسل ID المستخدم:")
        return

    # تفعيل اشتراك
    if text == "⭐ تفعيل اشتراك":
        login_state[chat_id] = {"step": "sub_user"}
        bot.send_message(chat_id, "أرسل ID المستخدم لتفعيل اشتراكه:")
        return

    # إلغاء اشتراك
    if text == "❌ إلغاء اشتراك":
        login_state[chat_id] = {"step": "unsub_user"}
        bot.send_message(chat_id, "أرسل ID المستخدم لإلغاء اشتراكه:")
        return

    # رسالة جماعية
    if text == "📢 رسالة جماعية":
        login_state[chat_id] = {"step": "broadcast"}
        bot.send_message(chat_id, "أرسل نص الرسالة لإرسالها للجميع:")
        return

    # ============================
    #      حالات الإدمن الفرعية
    # ============================

    if chat_id in login_state:
        state = login_state[chat_id]["step"]

        # فحص مستخدم
        if state == "check_user":
            try:
                user_id = int(text)
            except:
                bot.send_message(chat_id, "❌ ID غير صالح.")
                return

            user = db.get_user(user_id)
            msg_used = user[2]
            img_used = user[3]
            sub = "✔️ مشترك" if user[4] else "❌ غير مشترك"

            bot.send_message(chat_id,
                f"👤 معلومات المستخدم:\n\n"
                f"🆔 ID: {user_id}\n"
                f"✉️ الرسائل: {msg_used}/{config.FREE_MSG_LIMIT}\n"
                f"🖼️ الصور: {img_used}/{config.FREE_IMG_LIMIT}\n"
                f"⭐ الاشتراك: {sub}"
            )

            login_state.pop(chat_id, None)
            return

        # تفعيل اشتراك
        if state == "sub_user":
            try:
                user_id = int(text)
            except:
                bot.send_message(chat_id, "❌ ID غير صالح.")
                return

            db.set_subscription(user_id, True)
            bot.send_message(chat_id, f"⭐ تم تفعيل اشتراك المستخدم {user_id}.")

            try:
                bot.send_message(user_id, "⭐ تم تفعيل اشتراكك.")
            except:
                pass

            login_state.pop(chat_id, None)
            return

        # إلغاء اشتراك
        if state == "unsub_user":
            try:
                user_id = int(text)
            except:
                bot.send_message(chat_id, "❌ ID غير صالح.")
                return

            db.set_subscription(user_id, False)
            bot.send_message(chat_id, f"❌ تم إلغاء اشتراك المستخدم {user_id}.")

            try:
                bot.send_message(user_id, "❌ تم إلغاء اشتراكك.")
            except:
                pass

            login_state.pop(chat_id, None)
            return

        # رسالة جماعية
        if state == "broadcast":
            broadcast_text = text

            conn = db.sqlite3.connect(db.DB_NAME)
            c = conn.cursor()
            c.execute("SELECT tg_id FROM users")
            users = c.fetchall()
            conn.close()

            sent = 0
            for (uid,) in users:
                try:
                    bot.send_message(uid, broadcast_text)
                    sent += 1
                except:
                    pass

            bot.send_message(chat_id, f"📢 تم إرسال الرسالة إلى {sent} مستخدم.")
            login_state.pop(chat_id, None)
            return
