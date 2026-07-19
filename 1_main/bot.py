from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import aiohttp
import asyncio
from main import settings


bot = Bot(token=settings.bot_token)
dp = Dispatcher()

class AddTransactionForm(StatesGroup):
    amount = State()
    category = State()
    description = State()

@dp.message(F.text == "Добавить")
async def process_start(message: types.Message, state: FSMContext):
    await state.set_state(AddTransactionForm.amount)
    await message.answer("Введите сумму:")

@dp.message(AddTransactionForm.amount)
async def process_amount(message: types.Message, state: FSMContext):
    await state.update_data(amount=message.text)
    await state.set_state(AddTransactionForm.category)
    await message.answer("Введите категорию:")

@dp.message(AddTransactionForm.category)
async def process_category(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    await state.set_state(AddTransactionForm.description)
    await message.answer("Введите описание:")

@dp.message(AddTransactionForm.description)
async def process_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    payload = {
        "user_id": message.from_user.id,
        "amount": int(data.get("amount")),
        "category": data.get("category"),
        "description": data.get("description")
    }
    async with aiohttp.ClientSession() as session:
        async with session.post("http://127.0.0.1:8000/transactions", json=payload) as response:
            result = await response.json()
    await message.answer("Транзакция успешно добавлен!")
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")