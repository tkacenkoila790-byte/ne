import os, time, random, telebot
from telebot import types

# Вставьте ваш токен от @BotFather вместо ХХХ
bot = telebot.TeleBot('8908913545:AAFqVtBWMZNTrJQKGJxDPyi3wsSHC9iv77Y')
ADMIN_ID = 8455479648

# Временная база данных в памяти сервера для хранения балансов обычных пользователей
USER_BALANCES = {}

def get_balance(uid):
    if uid == ADMIN_ID:
        return 999999999.0  # Бесконечный баланс для создателя
    if uid not in USER_BALANCES:
        USER_BALANCES[uid] = 0.0  # У всех остальных изначально 0.00 USD
    return USER_BALANCES[uid]

def change_balance(uid, amount):
    if uid == ADMIN_ID:
        return  # У админа баланс не уменьшается и не увеличивается, всегда бесконечность
    if uid not in USER_BALANCES:
        USER_BALANCES[uid] = 0.0
    USER_BALANCES[uid] = max(0.0, round(USER_BALANCES[uid] + amount, 2))

M_MAIN = lambda name: (f"👋 *Здравствуй, {name}\\!* Ты попал в крипто\\-бота, основанного на базе решений *@send*\\.\n\n"
                       f"🛡️ _Данная компания полностью подтвердила, что этот бот не нарушает правил платформы Telegram, "
                       f"а также не занимается мошенническими схемами\\._")

def get_main_keyboard():
    m = types.InlineKeyboardMarkup(row_width=2)
    m.add(types.InlineKeyboardButton("💎 Мой Кошелёк", callback_data="wallet"), types.InlineKeyboardButton("🤝 P2P Маркет", callback_data="p2p"))
    m.add(types.InlineKeyboardButton("🕹️ Игровой Центр", callback_data="game_center"), types.InlineKeyboardButton("⚙️ Настройки", callback_data="settings"))
    return m

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, M_MAIN(m.from_user.first_name or "Друг"), parse_mode='MarkdownV2', reply_markup=get_main_keyboard())

@bot.callback_query_handler(func=lambda c: True)
def menu(c):
    uid, cid, mid = c.from_user.id, c.message.chat.id, c.message.message_id
    
    if c.data == "main_menu":
        bot.edit_message_text(M_MAIN(c.from_user.first_name or "Друг"), cid, mid, parse_mode='MarkdownV2', reply_markup=get_main_keyboard())
    
    # КРИПТО КОШЕЛЕК В СТИЛЕ @CryptoBot
    elif c.data == "wallet":
        bal_val = get_balance(uid)
        bal_str = "*∞ USD*" if uid == ADMIN_ID else f"`{bal_val:.2f} USD`"
        stat = "👑 Владелец" if uid == ADMIN_ID else "👤 Пользователь"
        
        # Структура как в оригинальном боте: баланс сверху, курсы валют списком снизу
        txt = (
            f"💎 *Ваш Кошелёк*\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"💵 Доступный баланс:\n"
            f"{bal_str} \\({stat}\\)\n\n"
            f"📊 *Курсы криптовалют под управлением @send:*\n"
            f"├ 💎 TON: `$5.42` \\(0.00 USD\\)\n"
            f"├ 🪙 BTC: `$64,250` \\(0.00 USD\\)\n"
            f"├ 🔷 ETH: `$3,420` \\(0.00 USD\\)\n"
            f"└ 💵 USDT: `$1.00` \\(0.00 USD\\)"
        )
        m = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("➕ Пополнить", callback_data="st"), 
            types.InlineKeyboardButton("📤 Вывести", callback_data="st")
        ).add(types.InlineKeyboardButton("⬅️ Меню", callback_data="main_menu"))
        bot.edit_message_text(txt, cid, mid, parse_mode='MarkdownV2', reply_markup=m)
        
    elif c.data == "p2p":
        txt = "🤝 *P2P Торговля*\n━━━━━━━━━━\n🏪 Безопасный обмен криптовалюты между пользователями\\.\n\n📌 *Объявления:* _активных предложений не найдено\\._"
        m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("➕ Создать", callback_data="st")).add(types.InlineKeyboardButton("⬅️ Меню", callback_data="main_menu"))
        bot.edit_message_text(txt, cid, mid, parse_mode='MarkdownV2', reply_markup=m)
        
    elif c.data == "game_center":
        bal_val = get_balance(uid)
        bal_str = "∞" if uid == ADMIN_ID else f"{bal_val:.2f}"
        txt = f"🕹️ *Игровой Центр @send*\n━━━━━━━━━━\n💵 Твой игровой баланс: `{bal_str} USD`\n\n🎰 Каждая ставка на игру стоит *10 USD*\\. Выберите дисциплину:"
        m = types.InlineKeyboardMarkup(row_width=2).add(
            types.InlineKeyboardButton("🚀 Ракетка", callback_data="g_rock"), 
            types.InlineKeyboardButton("🏀 Баскетбол", callback_data="g_b"), 
            types.InlineKeyboardButton("⚽ Футбол", callback_data="g_f"), 
            types.InlineKeyboardButton("🎯 Дротики", callback_data="g_d")
        ).add(types.InlineKeyboardButton("⬅️ Меню", callback_data="main_menu"))
        bot.edit_message_text(txt, cid, mid, parse_mode='MarkdownV2', reply_markup=m)
        
    # ИГРА РАКЕТКА С ИГРОВЫМИ СТАВКАМИ
    elif c.data == "g_rock" or c.data == "r_fly":
        if uid != ADMIN_ID and get_balance(uid) < 10.0:
            bot.answer_callback_query(c.id, text="❌ Недостаточно средств! Стоимость ставки — 10 USD", show_alert=True)
            return
            
        if c.data == "r_fly":
            change_balance(uid, -10.0) # Списание ставки
            cp = round(random.uniform(0.5, 4.5), 2) # Ракетка может взорваться и в убыток (< 1.0)
            
            for s in [1.00, round(cp*0.5, 2)]:
                if s < cp:
                    bot.edit_message_text(f"🚀 *Ракетка летит\\!* Множитель: `{s}x`", cid, mid, parse_mode='MarkdownV2')
                    time.sleep(0.4)
            
            if cp >= 1.0:
                win_amount = round(10.0 * cp, 2)
                change_balance(uid, win_amount)
                txt = f"🎉 *ВЫИГРЫШ\\!*\n━━━━━━━━━━\n📈 Раунд завершен: `{cp}x`\n💵 Начислено: `+{win_amount:.2f} USD`"
            else:
                txt = f"💥 *КРАШ В НАЧАЛЕ\\!*\n━━━━━━━━━━\n📈 Взрыв на отметке: `{cp}x`\n📉 Потеряно: `-10.00 USD`"
        else: 
            txt = "🚀 *Текстовая Ракетка*\n━━━━━━━━━━\n💰 Стоимость входа: *10 USD*\\.\nЖмите кнопку для старта\\! Успейте забрать куш до взрыва\\!"
            
        m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🛫 ЗАПУСК (10 USD)", callback_data="r_fly")).add(types.InlineKeyboardButton("⬅️ Игры", callback_data="game_center"))
        bot.edit_message_text(txt, cid, mid, parse_mode='MarkdownV2', reply_markup=m)
        
    # АНИМИРОВАННЫЕ ИГРЫ СО СТАВКАМИ
    elif c.data in ["g_b", "g_f", "g_d"]:
        if uid != ADMIN_ID and get_balance(uid) < 10.0:
            bot.answer_callback_query(c.id, text="❌ Недостаточно средств! Стоимость броска — 10 USD", show_alert=True)
            return
            
        bot.delete_message(cid, mid)
        change_balance(uid, -10.0) # Списание ставки
        
        emo = {"g_b": "🏀", "g_f": "⚽", "g_d": "🎯"}[c.data]
        res = bot.send_dice(cid, emoji=emo)
        time.sleep(2.5)
        
        val = res.dice.value
        is_win = False
        if emo == "🏀" and (val == 4 or val == 5): is_win = True
        elif emo == "⚽" and (val == 3 or val == 4 or val == 5): is_win = True
        elif emo == "🎯" and val == 6: is_win = True
        
        if is_win:
            change_balance(uid, 25.0) # Возврат ставки + чистый выигрыш 15 USD
            win = f"🎉 *ТОЧНОЕ ПОПАДАНИЕ\\!*\n💵 Выигрыш: `+25.00 USD` \\(+15 чистого бюджета\\)"
        else:
            win = "❌ *ПРОМАХ\\!*\n📉 Ставка `-10.00 USD` уходит в доход бота\\."
            
        m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔄 Бросить еще раз (10 USD)", callback_data=c.data), types.InlineKeyboardButton("⬅️ Игры", callback_data="game_center"))
        bot.send_message(cid, f"{win}\n━━━━━━━━━━\n📊 Системные очки: `{val}`", parse_mode='MarkdownV2', reply_markup=m)
        
    elif c.data == "settings":
        txt = "⚙️ *Настройки*\n━━━━━━━━━━\n🌐 Язык: *Русский*\n🪙 Валюта: *USD*\n📱 Телефон: _нет_"
        m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🌐 Язык", callback_data="st"), types.InlineKeyboardButton("📱 Телефон", callback_data="st")).add(types.InlineKeyboardButton("⬅️ Меню", callback_data="main_menu"))
        bot.edit_message_text(txt, cid, mid, parse_mode='MarkdownV2', reply_markup=m)
        
    elif c.data == "st":
        bot.answer_callback_query(c.id, text="⚡ Функция в разработке", show_alert=True)

if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)
