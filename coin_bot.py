
import os
import json
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("🌕 Орёл или решка"))
keyboard.add(KeyboardButton("💰 Баланс"))
keyboard.add(KeyboardButton("📤 Вывод звёзд"))

BALANCE_FILE = "balance.json"

def load_balances():
    if not os.path.exists(BALANCE_FILE):
        return {}
    with open(BALANCE_FILE, "r") as f:
        return json.load(f)

def save_balances(balances):
    with open(BALANCE_FILE, "w") as f:
        json.dump(balances, f)

def get_balance(user_id):
    balances = load_balances()
    return balances.get(str(user_id), 0)

def change_balance(user_id, amount):
    balances = load_balances()
    uid = str(user_id)
    balances[uid] = balances.get(uid, 0) + amount
    save_balances(balances)

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.answer("Привет! Бросай монету 🎯", reply_markup=keyboard)

@dp.message_handler(lambda m: m.text == "🌕 Орёл или решка")
async def coin_flip(msg: types.Message):
    user_id = msg.from_user.id
    balance = get_balance(user_id)
    if balance < 1:
        await msg.answer("У тебя недостаточно звёзд. Нужно хотя бы 1 ⭐.")
        return

    # Минус 1 звезда за попытку
    change_balance(user_id, -1)

    # 65% шанс победы бота
    bot_wins = random.random() < 0.65

    if bot_wins:
        result = "😈 Бот победил!"
    else:
        change_balance(user_id, 2)
        result = "🎉 Ты победил! Получаешь 2 ⭐!"

    await msg.answer(f"Результат: {result}")

@dp.message_handler(lambda m: m.text == "💰 Баланс")
async def show_balance(msg: types.Message):
    balance = get_balance(msg.from_user.id)
    await msg.answer(f"Твой баланс: ⭐ {balance}")

@dp.message_handler(lambda m: m.text == "📤 Вывод звёзд")
async def withdraw_request(msg: types.Message):
    user_id = msg.from_user.id
    balance = get_balance(user_id)
    await bot.send_message(ADMIN_ID, f"🔔 Запрос на вывод от @{msg.from_user.username or user_id} (ID: {user_id})
Баланс: ⭐ {balance}")
    await msg.answer("Запрос отправлен админу. Ожидай ответа.")

