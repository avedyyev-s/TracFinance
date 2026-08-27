from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def generate_keyboard_wallet(wallet_list):
    row_keyboard_list = []
    for wallet in wallet_list:
        row_keyboard_list.append([InlineKeyboardButton(text=f"{wallet["name"]}:  {wallet["balance"]} (руб.)", callback_data=f"wallet_select_{wallet["id"]}")])
    return InlineKeyboardMarkup(
        inline_keyboard=row_keyboard_list
    )

def generate_dashboard_keyboard(incomes_list, wallets_list, expenses_list):
    row_dashboard_keyboars_list = []
    current_row = []
    row_dashboard_keyboars_list.append([InlineKeyboardButton(text="─── 📈 ДОХОДЫ ───", callback_data="ignore")])
    for income in incomes_list:
        current_row.append(InlineKeyboardButton(text=f"{income["icon"]} {income["name"]}:  {income.get("amount", 0)}", callback_data=f"income_{income["id"]}"))
        if len(current_row) == 2:
            row_dashboard_keyboars_list.append(current_row)
            current_row = []
    if len(current_row) > 0:
        row_dashboard_keyboars_list.append(current_row)
        current_row = []
    row_dashboard_keyboars_list.append([InlineKeyboardButton(text=f"➕ Добавить категорию доход", callback_data="add_new_income")])
    row_dashboard_keyboars_list.append([InlineKeyboardButton(text="─── 💳 МОИ СЧЕТА ───", callback_data="ignore")])
    for wallet in wallets_list:
        current_row.append(InlineKeyboardButton(text=f"{wallet["name"]}:  {wallet["balance"]}", callback_data=f"wallet_info_{wallet["id"]}"))
        if len(current_row) == 2:
            row_dashboard_keyboars_list.append(current_row)
            current_row = []
    if len(current_row) > 0:
        row_dashboard_keyboars_list.append(current_row)
        current_row = []
    row_dashboard_keyboars_list.append([InlineKeyboardButton(text=f"➕ Добавить кошелек", callback_data="add_new_wallet")])
    row_dashboard_keyboars_list.append([InlineKeyboardButton(text="─── 📉 РАСХОДЫ ───", callback_data="ignore")])
    for expense in expenses_list:
        current_row.append(InlineKeyboardButton(text=f"{expense["icon"]} {expense["name"]}:  {expense.get("amount", 0)}", callback_data=f"expense_{expense["id"]}"))
        if len(current_row) == 2:
            row_dashboard_keyboars_list.append(current_row)
            current_row = []
    if len(current_row) > 0:
        row_dashboard_keyboars_list.append(current_row)
        current_row = []
    row_dashboard_keyboars_list.append([InlineKeyboardButton(text=f"➕ Добавить категорию расход", callback_data="add_new_expense")])
    return InlineKeyboardMarkup(
        inline_keyboard=row_dashboard_keyboars_list
    )

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎛️ Главная")],
        [KeyboardButton(text="📜 История"), KeyboardButton(text="📊 Аналитика")]
    ],
    resize_keyboard=True
)




