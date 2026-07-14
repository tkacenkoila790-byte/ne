import os, time, random, telebot
from telebot import types

# Вставьте ваш токен от @BotFather вместо ХХХ
bot = telebot.TeleBot('8908913545:AAFqVtBWMZNTrJQKGJxDPyi3wsSHC9iv77Y')
ADMIN_ID = 8455479648

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
    
    elif c.data == "wallet":
        bal, stat = ("*∞ USD*", "👑 Владелец") if uid == ADMIN_ID else ("`0.00 USD`", "👤 Пользователь")
        txt = f"💎 *Ваш Кошелёк*\n━━━━━━━━━━\n💵 Баланс: {bal}\n📊 Статус: {stat}\n\n_TON: $5\\.42 | BTC: $64,250_"
        m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("➕ Пополнить", callback_data="st"), types.InlineKeyboardButton("📤 Вывести", callback_data="st")).add(types.InlineKeyboardButton("⬅️ Меню", callback_data="main_menu"))
        bot.edit_message_text(txt, cid, mid, parse_mode='MarkdownV2', reply_markup=m)
        
    elif c.data == "p2p":
        txt = "🤝 *P2P Торговля*\n━━━━━━━━━━\n🏪 Безопасный обмен криптовалюты\\.\n\n📌 *Объявления:* _пусто\\._"
        m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("➕ Создать", callback_data="st")).add(types.InlineKeyboardButton("⬅️ Меню", callback_data="main_menu"))
        bot.edit_message_text(txt, cid, mid, parse_mode='MarkdownV2', reply_markup=m)
        
    elif c.data == "game_center":
        txt = "🕹️ *Игровой Центр @send*\n━━━━━━━━━━\n🎰 Выберите игру из списка ниже:"
        m = types.InlineKeyboardMarkup(row_width=2).add(types.InlineKeyboardButton("🚀 Ракетка", callback_data="g_rock"), types.InlineKeyboardButton("🏀 Баскетбол", callback_data="g_b"), types.InlineKeyboardButton("⚽ Футбол", callback_data="g_f"), types.InlineKeyboardButton("🎯 Дротики", callback_data="g_d")).add(types.InlineKeyboardButton("⬅️ Меню", callback_data="main_menu"))
        bot.edit_message_text(txt, cid, mid, parse_mode='MarkdownV2', reply_markup=m)
        
    elif c.data == "g_rock" or c.data == "r_fly":
        if c.data == "r_fly":
            cp = round(random.uniform(1.1, 4.5), 2)
            for s in [1.00, round(cp*0.5, 2)]:
                if s < cp:
                    bot.edit_message_text(f"🚀 *Ракетка летит\\!* Множитель: `{s}x`", cid, mid, parse_mode='MarkdownV2')
                    time.sleep(0.4)
            txt = f"💥 *ВЗРЫВ\\!*\n━━━━━━━━━━\n📈 График остановился: `{cp}x`"
        else: txt = "🚀 *Текстовая Ракетка*\n━━━━━━━━━━\nЖмите кнопку для старта\\! Успейте забрать куш до взрыва\\!"
        m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🛫 ЗАПУСК", callback_data="r_fly")).add(types.InlineKeyboardButton("⬅️ Игры", callback_data="game_center"))
        bot.edit_message_text(txt, cid, mid, parse_mode='MarkdownV2', reply_markup=m)
        
    elif c.data in ["g_b", "g_f", "g_d"]:
        bot.delete_message(cid, mid)
        emo = {"g_b": "🏀", "g_f": "⚽", "g_d": "🎯"}[c.data]
        res = bot.send_dice(cid, emoji=emo)
        time.sleep(2.5)
        win = "🎉 *ГОЛ / ПОПАДАНИЕ\\!*" if (emo=="🏀" and res.dice.value in) or (emo=="⚽" and res.dice.value in) or (emo=="🎯" and res.dice.value==6) else "❌ *ПРОМАХ\\!*"
        m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔄 Еще раз", callback_data=c.data), types.InlineKeyboardButton("⬅️ Игры", callback_data="game_center"))
        bot.send_message(cid, f"{win}\n━━━━━━━━━━\n📊 Очки: `{res.dice.value}`", parse_mode='MarkdownV2', reply_markup=m)
        
    elif c.data == "settings":
        txt = "⚙️ *Настройки*\n━━━━━━━━━━\n🌐 Язык: *Русский*\n🪙 Валюта: *USD*\n📱 Телефон: _нет_"
        m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🌐 Язык", callback_data="st"), types.InlineKeyboardButton("📱 Телефон", callback_data="st")).add(types.InlineKeyboardButton("⬅️ Меню", callback_data="main_menu"))
        bot.edit_message_text(txt, cid, mid, parse_mode='MarkdownV2', reply_markup=m)
        
    elif c.data == "st":
        bot.answer_callback_query(c.id, text="⚡ Функция в разработке", show_alert=True)

if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)
