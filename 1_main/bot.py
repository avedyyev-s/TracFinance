import aiohttp
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from main import settings
import keyboards as kb

bot = Bot(token=settings.bot_token)
dp = Dispatcher()

class AddTransactionForm(StatesGroup):
    wallet = State()
    transaction_type = State()
    amount = State()
    category = State()
    description = State()

class DeleteTransactionForm(StatesGroup):
    transaction_id = State()

class AddWalletForm(StatesGroup):
    name = State()
    balance = State()

class AddCategoryForm(StatesGroup):
    name = State()

async def send_api_request(endpoint, method="GET", payload=None):
    basic_request = "http://127.0.0.1:8000"
    url_adress = basic_request + endpoint
    try:
        async with aiohttp.ClientSession() as session:
            if method == "POST":
                async with session.post(url_adress, json=payload) as response:
                    response.raise_for_status()
                    result = await response.json()
                    return result
            elif method == "DELETE":
                async with session.delete(url_adress) as response:
                    response.raise_for_status()
                    return True
            else:
                async with session.get(url_adress) as response:
                    response.raise_for_status()
                    result = await response.json()
                    return result
    except aiohttp.ClientResponseError as error:
        print(f"Ошибка сервера! Статус: {error.status}, Сообщение: {error.message}")
        return None
    except aiohttp.ClientConnectionError:
        print("Сервер недоступен")
        return None

async def dashboard(user_id: int):
    wallets = await send_api_request(f"/wallets/{user_id}")
    incomes = await send_api_request(f"/categories/{user_id}/income")
    expenses = await send_api_request(f"/categories/{user_id}/expense")
    data = wallets.get("wallets")
    total_balance = sum([item["balance"] for item in data])
    keyboard = kb.generate_dashboard_keyboard(incomes.get("categories", []), wallets.get("wallets", []), expenses.get("categories", []))
    return total_balance, keyboard

@dp.message(Command("start"))
async def command_start(message: Message):
    try:
        await message.answer("start", reply_markup=kb.menu)
        await message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение: {e}")

@dp.message(F.text == "🎛️ Главная")
async def process_income(message: Message):
    await message.delete()
    balance, keyboard = await dashboard(message.from_user.id)
    await message.answer(f"ГЛАВНАЯ\nОбщий баланс: {balance} \n", reply_markup=keyboard)

@dp.callback_query(F.data == "add_new_wallet")
async def process_add_new_wallet(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)
    await state.set_state(AddWalletForm.name)
    await callback.message.answer("Введите название:")

@dp.message(AddWalletForm.name)
async def process_save_new_wallet_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddWalletForm.balance)
    await message.answer("Введите начальный баланс:")

@dp.message(AddWalletForm.balance)
async def process_save_new_wallet_balance(message: Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        if float(message.text) >= 0:
            await state.update_data(balance=float(message.text))
        else:
            await message.answer("Сумма должна положительной!")
            return
    except ValueError:
        await message.answer("Введите цифрами!")
        return   
    data = await state.get_data()
    payload = {
        "user_id": user_id,
        "name": data.get("name"),
        "balance": data.get("balance")
    }
    request = await send_api_request(f"/wallets", "POST", payload)
    balance, keyboard = await dashboard(user_id)
    await message.answer(f"ГЛАВНАЯ\nОбщий баланс: {balance} \n", reply_markup=keyboard)
    await state.clear()

@dp.callback_query(F.data == "add_new_income")
async def process_add_new_income(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)
    await state.update_data(transaction_type="income")
    await state.set_state(AddCategoryForm.name)
    await callback.message.answer("Введите название:")

@dp.callback_query(F.data == "add_new_expense")
async def process_add_new_expense(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)
    await state.update_data(transaction_type="expense")
    await state.set_state(AddCategoryForm.name)
    await callback.message.answer("Введите название:")

@dp.message(AddCategoryForm.name)
async def process_save_new_category(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    transaction_type = data.get("transaction_type")
    payload = {
        "user_id": user_id,
        "name": message.text,
        "category_type": transaction_type,
        "icon": "🏷️"
    }
    request = await send_api_request(f"/categories", "POST", payload)
    balance, keyboard = await dashboard(user_id)
    await state.update_data(category_id=request.get("category_id"))
    new_data = await state.get_data()
    if new_data.get("transaction_type") == "income":
        await message.answer(f"ГЛАВНАЯ\nОбщий баланс: {balance} \n", reply_markup=keyboard)
        await state.clear()
    else:
        await message.answer(f"ГЛАВНАЯ\nОбщий баланс: {balance} \n", reply_markup=keyboard)
        await state.clear()

@dp.callback_query(F.data.startswith("income_"))
async def process_add_new_income_category(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)
    category_id = int(callback.data.split("_")[1])
    await state.update_data(category_id=category_id)
    await state.update_data(transaction_type="income")
    await state.set_state(AddTransactionForm.wallet)
    request = await send_api_request(f"/wallets/{user_id}")
    keyboard = kb.generate_keyboard_wallet(request.get("wallets"))
    await callback.message.answer("Выберите кошелек:", reply_markup=keyboard)

@dp.callback_query(F.data.startswith("expense_"))
async def process_add_new_expense_category(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)
    category_id = int(callback.data.split("_")[1])
    await state.update_data(category_id=category_id)
    await state.update_data(transaction_type="expense")
    await state.set_state(AddTransactionForm.wallet)
    request = await send_api_request(f"/wallets/{user_id}")
    keyboard = kb.generate_keyboard_wallet(request.get("wallets"))
    await callback.message.answer("Выберите кошелек:", reply_markup=keyboard)

@dp.callback_query(AddTransactionForm.wallet, F.data.startswith("wallet_select_"))
async def process_chose_wallet(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)
    wallet_id = int(callback.data.split("_")[2])
    await state.update_data(wallet_id=wallet_id)
    await state.set_state(AddTransactionForm.amount)
    await callback.message.answer("Введите сумму:")

@dp.message(AddTransactionForm.amount)
async def process_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text)
        if amount > 0:
            await state.update_data(amount=amount)
            await state.set_state(AddTransactionForm.description)
            await message.answer(f"Описание:\nЧтобы пропустить отправьте -")
        else:
            await message.answer("Сумма должна быть положительной либо больше нуля")
    except ValueError:
        await message.answer("Некорректный ввод! Введите цифрами!")
        return

@dp.message(AddTransactionForm.description)
async def process_description(message: Message, state: FSMContext):
    user_id = message.from_user.id
    new_description = message.text
    if new_description == "-":
        new_description = ""
    await state.update_data(description=new_description)
    data = await state.get_data()
    payload = {
        "user_id": user_id,
        "wallet_id": data.get("wallet_id"),
        "category_id": data.get("category_id"),
        "transaction_type": data.get("transaction_type"),
        "amount": data.get("amount"),
        "description": data.get("description")
    }
    request = await send_api_request(f"/transactions", "POST", payload)
    balance, keyboard = await dashboard(user_id)
    if request == None:
        await message.answer("Не удалось совершить операцию. Попробуйте еще раз!")
        await message.answer(f"ГЛАВНАЯ\nОбщий баланс: {balance} \n", reply_markup=keyboard)
        await state.clear()
        return
    else:
        await message.answer("Операция успешно совершена!")
        await message.answer(f"ГЛАВНАЯ\nОбщий баланс: {balance} \n", reply_markup=keyboard)
        await state.clear()

@dp.callback_query(F.data == "ignore")
async def process_ignore(callback: CallbackQuery):
    await callback.answer()

@dp.callback_query(F.data.startswith("wallet_info_"))
async def process_wallet_info(callback: CallbackQuery):
    await callback.answer("Это ваш кошелек")


@dp.message(F.text == "📜 История")
async def process_history(message: Message, state: FSMContext):
    user_id = message.from_user.id
    request = await send_api_request(f"/transactions/{user_id}")
    if request == None:
        await message.answer("Сервис временно недоступен. Попробуйте позже!")
        return
    data = request.get("transactions")
    if len(data) == 0:
        balance, keyboard = await dashboard(user_id)
        await message.answer("📜 История операций пуста", reply_markup=keyboard)
    else:
        sum_income = 0.0
        sum_expense = 0.0
        
        lines = []        
        for item in data:
            icon_operation = ""
            if item["transaction_type"] == "income":
                icon_operation = "🟢 +"
                sum_income += item['amount']
            else:
                icon_operation = "🔴 -"
                sum_expense += item['amount']
            if len(lines) < 20:
                lines.append(f"{item['category_icon']} {item['category_name']} ({item['wallet_name']})\n{icon_operation}{item['amount']} руб. • {item['transaction_date'][0:10]}")

        saldo = sum_income - sum_expense
        text_header = (f"⚖️ Сальдо: {saldo:.2f} руб.\n\n📈 Поступления: +{sum_income:.2f} руб.\n\n📉 Списания: -{sum_expense:.2f} руб. \n━━━━━━━━━━━━━━━━━━━━━\n📋 Последние операции:\n\n")
        finally_text = text_header + "\n\n".join(lines)
        await message.answer(finally_text)
        









async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")