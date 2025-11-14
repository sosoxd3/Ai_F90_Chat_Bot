# -*- coding: utf-8 -*-
"""
database.py
ملف قاعدة البيانات الخاصة ببوت Ai F90 Chat Bot
"""

import sqlite3

DB_NAME = "f90.db"

# ===============================
#   إنشاء قاعدة البيانات
# ===============================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER UNIQUE,
        msgs_used INTEGER DEFAULT 0,
        imgs_used INTEGER DEFAULT 0,
        subscribed INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()


# ===============================
#   جلب مستخدم أو إنشاؤه
# ===============================
def get_user(tg_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # هل المستخدم موجود؟
    c.execute("SELECT * FROM users WHERE tg_id=?", (tg_id,))
    row = c.fetchone()

    # لو مش موجود → ننشئه
    if not row:
        c.execute("INSERT INTO users (tg_id) VALUES (?)", (tg_id,))
        conn.commit()
        c.execute("SELECT * FROM users WHERE tg_id=?", (tg_id,))
        row = c.fetchone()

    conn.close()
    return row
    # إرجاع الصف:
    # (id, tg_id, msgs_used, imgs_used, subscribed)


# ===============================
#   تحديث عداد الرسائل والصور
# ===============================
def update_usage(tg_id, msg_inc=0, img_inc=0):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    UPDATE users
    SET msgs_used = msgs_used + ?, imgs_used = imgs_used + ?
    WHERE tg_id=?
    """, (msg_inc, img_inc, tg_id))

    conn.commit()
    conn.close()


# ===============================
#   تفعيل أو إلغاء الاشتراك
# ===============================
def set_subscription(tg_id, status: bool):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("UPDATE users SET subscribed=? WHERE tg_id=?", (1 if status else 0, tg_id))

    conn.commit()
    conn.close()


# ===============================
#   فحص اشتراك مستخدم
# ===============================
def is_subscribed(tg_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT subscribed FROM users WHERE tg_id=?", (tg_id,))
    row = c.fetchone()

    conn.close()
    return bool(row[0]) if row else False


# ===============================
#   جلب عداد الاستخدام
# ===============================
def get_usage(tg_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT msgs_used, imgs_used FROM users WHERE tg_id=?", (tg_id,))
    row = c.fetchone()

    conn.close()
    return row if row else (0, 0)
