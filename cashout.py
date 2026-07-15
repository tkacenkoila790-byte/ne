import asyncio
import random
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Создаем роутер вместо диспетчера
router = Router()

# Подключаем фейковую базу данных из главного файла (импортируем ниже)
from bot import users_db, get_main_menu

# Состояния для отслеживания шагов пользователя (FSM)
class CashoutStates(StatesGroup):
    waiting_for_card = State()
    waiting_for_amount = State()

# Меню выбора способа вывода
def get_cashout_menu():
    kb = [
        [KeyboardButton(text="💳 На банковскую карту"), KeyboardButton(text="📲 Через СБП")],
        [KeyboardButton(text="🔙 Главное меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# Кнопка "Вывод средств"
@router.message(F.text == "💳 Вывод средств")
async def cashout_options(message: Message):
    await message.answer("Выберите платежную систему для вывода средств:", reply_markup=get_cashout_menu())

# Нажатие на "На банковскую карту" (Запуск фейкового вывода)
@router.message(F.text == "💳 На банковскую карту")
async def card_cashout_start(message: Message, state: FSMContext):
    await message.answer(
        "Введите номер вашей банковской карты (16 цифр без пробелов):\n"
        "*Поддерживаются карты: МИР, Visa, Mastercard*",
        parse_mode="Markdown"
    )
    await state.set_state(CashoutStates.waiting_for_card)

# Шаг получения карты
@router.message(CashoutStates.waiting_for_card)
async def process_card(message: Message, state: FSMContext):
    card_number = message.text.replace(" ", "")
    
    if not card_number.isdigit() or len(card_number) < 16 or len(card_number) > 19:
        await message.answer("❌ Неверный формат карты. Введите 16 цифр номера карты:")
        return

    await state.update_data(card=card_number)
    await message.answer("Введите сумму вывода в рублях:")
    await state.set_state(CashoutStates.waiting_for_amount)

# Шаг получения суммы и имитация отправки
@router.message(CashoutStates.waiting_for_amount)
async def process_amount(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_balance = users_db.get(user_id, {"balance": 0})["balance"]
    
    if not message.text.isdigit():
        await message.answer("❌ Сумма должна быть числом. Введите сумму цифрами:")
        return
        
    amount = int(message.text)
    
    if amount <= 0:
        await message.answer("❌ Сумма должна быть больше 0.")
        return
        
    if amount > user_balance:
        await message.answer(f"❌ Недостаточно средств. Ваш баланс: {user_balance} руб.")
        await state.clear()
        return

    data = await state.get_data()
    card_num = data['card']
    
    # Списываем баланс внутри бота
    users_db[user_id]["balance"] -= amount
    await state.clear()

    hidden_card = f"{card_num[:4]}********{card_num[-4:]}"
    order_id = random.randint(100000, 999999)

    status_msg = await message.answer("⏳ *Установка соединения с банковским шлюзом...*", parse_mode="Markdown")
    await asyncio.sleep(2)
    await status_msg.edit_text("⏳ *Проверка транзакции сектором безопасности Anti-Fraud...*", parse_mode="Markdown")
    await asyncio.sleep(3)
    await status_msg.edit_text("⏳ *Авторизация платежа банком-эмитентом...*", parse_mode="Markdown")
    await asyncio.sleep(2)

    await status_msg.delete()
    await message.answer(
        f"✅ **Заявка на вывод №{order_id} успешно создана!**\n\n"
        f"💰 Сумма: `{amount} руб.`\n"
        f"💳 На карту: `{hidden_card}`\n"
        f"⏱ Статус: `В обработке банком`\n\n"
        f"Средства обычно поступают в течение 10-60 минут. Спасибо, что пользуетесь **ping-wallet**!",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )

# Фейковый вывод через СБП
@router.message(F.text == "📲 Через СБП")
async def sbp_cashout(message: Message):
    await message.answer("⚠️ Вывод через СБП временно недоступен из-за технических работ на стороне шлюза. Пожалуйста, используйте вывод на карту.")
