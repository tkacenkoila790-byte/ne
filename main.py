import os, sys

try:
    import telebot
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI"])
    import telebot

import time, random
from telebot import types

# Твой токен и ID владельца
bot = telebot.TeleBot('8908913545:AAFqVtBWMZNTrJQKGJxDPyi3wsSHC9iv77Y')
ADMIN_ID = 8455479648

USER_BALANCES = {}

def get_balance(uid):
    if uid == ADMIN_ID: return 999999999.0
    if uid not in USER_BALANCES: USER_BALANCES[uid] = 0.0
    return USER_BALANCES[uid]

def change_balance(uid, amount):
    if uid == ADMIN_ID: return
    if uid not in USER_BALANCES: USER_BALANCES[uid] = 0.0
    USER_BALANCES[uid] = max(0.0, round(USER_BALANCES[uid] + amount, 2))

# Приветственный текст на надежном HTML
def get_main_text(name):
    return (f"👋 <b>Здравствуй, {name}!</b> Ты попал в крипто-бота, основанного на базе решений <b>@send</b>.\n\n"
            f"🛡️ <i>Данная компания полностью подтвердила, что этот бот не нарушает правил платформы Telegram, "
            f"а также не занимается мошенническими схемами.</i>")

def get_main_keyboard():
    m = types.InlineKeyboardMarkup(row_width=2)
    m.add(types.InlineKeyboardButton("💎 Мой Кошелёк", callback_data="wallet"), types.InlineKeyboardButton("🤝 P2P Маркет", callback_data="p2p"))
    m.add(types.InlineKeyboardButton("🕹️ Игровой Центр", callback_data="game_center"), types.InlineKeyboardButton("⚙️ Настройки", callback_data="settings"))
    return m

# Админ-команда /mani
@bot.message_handler(commands=['mani'])
def admin_give_money(m):
    if m.from_user.id != ADMIN_ID:
        bot.reply_to(m, "❌ <b>У вас нет доступа к этой команде!</b>", parse_mode='HTML')
        return
    args = m.text.split()
    amount = 50000.0
    if len(args) > 1:
        try: amount = float(args[1])
        except ValueError:
            bot.reply_to(m, "❌ <b>Неверный формат суммы!</b> Пример: <code>/mani 1000</code>", parse_mode='HTML')
            return
    bot.reply_to(m, f"💰 <b>Владелец!</b> Баланс успешно пополнен на <code>{amount:,.2f} USD</code>.\n👑 Ваш текущий статус кошелька: <b>Бесконечность</b>", parse_mode='HTML')

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, get_main_text(m.from_user.first_name or "Друг"), parse_mode='HTML', reply_markup=get_main_keyboard())

@bot.callback_query_handler(func=lambda c: True)
def menu(c):
    uid, cid, mid = c.from_user.id, c.message.chat.id, c.message.message_id
    
    if c.data == "main_menu":
        bot.edit_message_text(get_main_text(c.from_user.first_name or "Друг"), cid, mid, parse_mode='HTML', reply_markup=get_main_keyboard())
    
    elif c.data == "wallet":
        bal_val = get_balance(uid)
        bal_str = "<b>∞ USD</b>" if uid == ADMIN_ID else f"<code>{bal_val:.2f} USD</code>"
        stat = "👑 Владелец" if uid == ADMIN_ID else "👤 Пользователь"
        txt = (f"💎 <b>Ваш Кошелёк</b>\n"
               f"━━━━━━━━━━━━━━━━━━\n"
               f"💵 Доступный баланс:\n"
               f"{bal_str} ({stat})\n\n"
               f"📊 <b>Курсы криптовалют под управлением @send:</b>\n"
               f"├ 💎 TON: <code>$5.42</code> (0.00 USD)\n"
               f"├ 🪙 BTC: <code>$64,250</code> (0.00 USD)\n"
               f"├ 🔷 ETH: <code>$3,420</code> (0.00 USD)\n"
               f"└ 💵 USDT: <code>$1.00</code> (0.00 USD)")
        m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("➕ Пополнить", callback_data="st"), types.InlineKeyboardButton("📤 Вывести", callback_data="st")).add(types.InlineKeyboardButton("⬅️ Меню", callback_data="main_menu"))
        bot.edit_message_text(txt, cid, mid, parse_mode='HTML', reply_markup=m)
        
    elif c.data == "p2p":
        txt = "🤝 <b>P2P Торговля</b>\n━━━━━━━━━━\n🏪 Безопасный обмен криптовалюты между пользователями.\n\n📌 <b>Объявления:</b> <i>активных предложений не найдено.</i>"
        m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("➕ Создать", callback_data="st")).add(types.InlineKeyboardButton("⬅️ Меню", callback_data="main_menu"))
        bot.edit_message_text(txt, cid, mid, parse_mode='HTML', reply_markup=m)
        
    elif c.data == "game_center":
        bal_val = get_balance(uid)
        bal_str = "∞" if uid == ADMIN_ID else f"{bal_val:.2f}"
        txt = f"🕹️ <b>Игровой Центр @send</b>\n━━━━━━━━━━\n💵 Твой игровой баланс: <code>{bal_str} USD</code>\n\n🎰 Каждая ставка на игру стоит <b>10 USD</b>. Выберите дисциплину:"
        m = types.InlineKeyboardMarkup(row_width=2).add(types.InlineKeyboardButton("🚀 Ракетка", callback_data="g_rock"), types.InlineKeyboardButton("🏀 Баскетбол", callback_data="g_b"), types.InlineKeyboardButton("⚽ Футбол", callback_data="g_f"), types.InlineKeyboardButton("🎯 Дротики", callback_data="g_d")).add(types.InlineKeyboardButton("⬅️ Меню", callback_data="main_menu"))
        bot.edit_message_text(txt, cid, mid, parse_mode='HTML', reply_markup=m)
        
    elif c.data == "g_rock" or c.data == "r_fly":
        if uid != ADMIN_ID and get_balance(uid) < 10.0:
            bot.answer_callback_query(c.id, text="❌ Недостаточно средств! Стоимость ставки — 10 USD", show_alert=True)
            return
        if c.data == "r_fly":
            change_balance(uid, -10.0)
            cp = round(random.uniform(0.5, 4.5), 2)
            for s in [1.00, round(cp*0.5, 2)]:
                if s < cp:
                    bot.edit_message_text(f"🚀 <b>Ракетка летит!</b> Множитель: <code>{s}x</code>", cid, mid, parse_mode='HTML')
                    time.sleep(0.4)
            if cp >= 1.0:
                win_amount = round(10.0 * cp, 2)
                change_balance(uid, win_amount)
                txt = f"🎉 <b>ВЫИГРЫШ!</b>\n━━━━━━━━━━\n📈 Раунд завершен: <code>{cp}x</code>\n💵 Начислено: <code>+{win_amount:.2f} USD</code>"
            else:
                txt = f"💥 <b>КРАШ В НАЧАЛЕ!</b>\n━━━━━━━━━━\n📈 Взрыв на отметке: <code>{cp}x</code>\n📉 Потеряно: <code>-10.00 USD</code>"
        else: txt = "🚀 <b>Текстовая Ракетка</b>\n━━━━━━━━━━\n💰 Стоимость входа: <b>10 USD</b>.\nЖмите кнопку для старта! Успейте забрать куш до взрыва!"
        m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🛫 ЗАПУСК (10 USD)", callback_data="r_fly")).add(types.InlineKeyboardButton("⬅️ Игры", callback_data="game_center"))
        bot.edit_message_text(txt, cid, mid, parse_mode='HTML', reply_markup=m)
        
    elif c.data in ["g_b", "g_f", "g_d"]:
        if uid != ADMIN_ID and get_balance(uid) < 10.0:
            bot.answer_callback_query(c.id, text="❌ Недостаточно средств! Стоимость броска — 10 USD", show_alert=True)
            return
        bot.delete_message(cid, mid)
        change_balance(uid, -10.0)
        emo = {"g_b": "🏀", "g_f": "⚽", "g_d": "🎯"}[c.data]
        res = bot.send_dice(cid, emoji=emo)
        time.sleep(2.5)
        val = res.dice.value
        is_win = (emo == "🏀" and (val == 4 or val == 5)) or (emo == "⚽" and (val == 3 or val == 4 or val == 5)) or (emo == "🎯" and val == 6)
        if is_win:
            change_balance(uid, 25.0)
            win = f"🎉 <b>ТОЧНОЕ ПОПАДАНИЕ!</b>\n💵 Выигрыш: <code>+25.00 USD</code>"
        else: win = "❌ <b>ПРОМАХ!</b>\n📉 Ставка <code>-10.00 USD</code> уходит в доход бота."
        m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔄 Бросить еще раз (10 USD)", callback_data=c.data), types.InlineKeyboardButton("⬅️ Игры", callback_data="game_center"))
        bot.send_message(cid, f"{win}\n━━━━━━━━━━\n📊 Системные очки: <code>{val}</code>", parse_mode='HTML', reply_markup=m)
        
    elif c.data == "settings":
        txt = "⚙️ <b>Настройки</b>\n━━━━━━━━━━\n🌐 Язык: <b>Русский</b>\n🪙 Валюта: <b>USD</b>\n📱 Телефон: <i>нет</i>"
        m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🌐 Язык", callback_data="st"), types.InlineKeyboardButton("📱 Телефон", callback_data="st")).add(types.InlineKeyboardButton("⬅️ Меню", callback_data="main_menu"))
        bot.edit_message_text(txt, cid, mid, parse_mode='HTML', reply_markup=m)
        
    elif c.data == "st":
        bot.answer_callback_query(c.id, text="⚡ Функция в разработке", show_alert=True)

if __name__ == '__main__':
    try: bot.remove_webhook()
    except: pass
    time.sleep(2.0)
    bot.infinity_polling(skip_pending=True)
