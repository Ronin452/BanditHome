import os
import sqlite3

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN не задан")


# ---------- БАЗА ДАННЫХ ----------

def init_db():
    conn = sqlite3.connect("bandit.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            coins INTEGER DEFAULT 100,
            level INTEGER DEFAULT 1,
            xp INTEGER DEFAULT 0,
            wins INTEGER DEFAULT 0,
            streak INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


def add_user(user):
    conn = sqlite3.connect("bandit.db")

    conn.execute("""
        INSERT OR IGNORE INTO users
        (user_id, username, first_name)
        VALUES (?, ?, ?)
    """, (
        user.id,
        user.username,
        user.first_name
    ))

    conn.commit()
    conn.close()


def get_user(user_id):
    conn = sqlite3.connect("bandit.db")

    user = conn.execute("""
        SELECT coins, level, xp, wins, streak
        FROM users
        WHERE user_id = ?
    """, (user_id,)).fetchone()

    conn.close()
    return user


# ---------- КЛАВИАТУРА ----------

def main_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("👤 Профиль", callback_data="profile"),
            InlineKeyboardButton("💰 Баланс", callback_data="balance")
        ],
        [
            InlineKeyboardButton("🎮 Игры", callback_data="games"),
            InlineKeyboardButton("🏆 Рейтинг", callback_data="rating")
        ],
        [
            InlineKeyboardButton("🎁 Бонус", callback_data="bonus"),
            InlineKeyboardButton("🛒 Магазин", callback_data="shop")
        ],
        [
            InlineKeyboardButton("💎 Донат", callback_data="donate"),
            InlineKeyboardButton("⚙️ Настройки", callback_data="settings")
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


# ---------- /START ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    add_user(user)

    text = (
        "🏠 <b>BANDIT HOME</b>\n\n"
        f"👋 Привет, <b>{user.first_name}</b>!\n\n"
        "🎮 Добро пожаловать в твой игровой дом.\n"
        "💰 Зарабатывай монеты\n"
        "⭐ Повышай уровень\n"
        "🏆 Попадай в рейтинг\n"
        "🎁 Забирай бонусы\n\n"
        "Выбери раздел ниже 👇"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=main_keyboard()
    )


# ---------- КНОПКИ ----------

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    user = get_user(user_id)

    if data == "profile":
        coins, level, xp, wins, streak = user

        text = (
            "👤 <b>ТВОЙ ПРОФИЛЬ</b>\n\n"
            f"👤 {query.from_user.first_name}\n"
            f"💰 Монеты: <b>{coins}</b>\n"
            f"⭐ Уровень: <b>{level}</b>\n"
            f"✨ XP: <b>{xp}</b>\n"
            f"🏆 Побед: <b>{wins}</b>\n"
            f"🔥 Серия: <b>{streak}</b>"
        )

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="home")]
            ])
        )

    elif data == "balance":
        coins = user[0]

        await query.edit_message_text(
            f"💰 <b>ТВОЙ БАЛАНС</b>\n\n"
            f"🪙 Монеты: <b>{coins}</b>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="home")]
            ])
        )

    elif data == "games":
        await query.edit_message_text(
            "🎮 <b>ИГРЫ</b>\n\n"
            "Скоро здесь появятся игры:\n\n"
            "🎲 Кубики\n"
            "✂️ Камень • Ножницы • Бумага\n"
            "🧠 Викторина\n"
            "⚡ Дуэли\n"
            "🎯 Угадай число",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="home")]
            ])
        )

    elif data == "rating":
        await query.edit_message_text(
            "🏆 <b>РЕЙТИНГ</b>\n\n"
            "🥇 Скоро здесь появятся лучшие игроки Bandit Home!",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="home")]
            ])
        )

    elif data == "bonus":
        await query.edit_message_text(
            "🎁 <b>ЕЖЕДНЕВНЫЙ БОНУС</b>\n\n"
            "Система ежедневных бонусов скоро будет доступна.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="home")]
            ])
        )

    elif data == "shop":
        await query.edit_message_text(
            "🛒 <b>МАГАЗИН</b>\n\n"
            "Здесь будут продаваться предметы, VIP и другие улучшения.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="home")]
            ])
        )

    elif data == "donate":
        await query.edit_message_text(
            "💎 <b>ДОНАТ</b>\n\n"
            "Скоро здесь появится система доната за Telegram Stars ⭐",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="home")]
            ])
        )

    elif data == "settings":
        await query.edit_message_text(
            "⚙️ <b>НАСТРОЙКИ</b>\n\n"
            "Настройки Bandit Home появятся здесь.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="home")]
            ])
        )

    elif data == "home":
        await query.edit_message_text(
            "🏠 <b>BANDIT HOME</b>\n\n"
            "Выбери нужный раздел 👇",
            parse_mode="HTML",
            reply_markup=main_keyboard()
        )


# ---------- ЗАПУСК ----------

def main():
    init_db()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    print("🏠 Bandit Home запущен!")

    app.run_polling()


if __name__ == "__main__":
    main()
