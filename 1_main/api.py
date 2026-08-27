from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from models import Transaction, Wallet, Category
from main import repository
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class TransactionCreate(BaseModel):
    user_id: int
    wallet_id: int
    category_id: int
    transaction_type: str
    amount: float
    description: str

class WalletCreate(BaseModel):
    user_id: int
    name: str
    balance: float

class CategoryCreate(BaseModel):
    user_id: int
    name: str
    category_type: str
    icon: str

@app.post("/transactions")
async def create_user_transaction(payload: TransactionCreate):
    transaction_instance = Transaction(
        transaction_id=0,
        user_id=payload.user_id,
        wallet_id=payload.wallet_id,
        category_id=payload.category_id,
        transaction_type=payload.transaction_type,
        amount=payload.amount,
        description=payload.description
    )
    return {"transaction_id": await repository.add_transaction(transaction_instance)}

@app.get("/transactions/{user_id}")
async def get_user_transactions(user_id: int):
    return {"transactions": await repository.get_transactions(user_id)}

@app.delete("/transactions/{transaction_id}")
async def del_user_transaction(transaction_id: int):
    transaction_delete = await repository.delete_transaction(transaction_id)
    return {"delete_transaction": "successfully deleted"}

@app.post("/wallets")
async def create_user_wallet(payload: WalletCreate):
    wallet_instance = Wallet(
        wallet_id=0,
        user_id=payload.user_id,
        name=payload.name,
        balance=payload.balance
    )
    return {"wallet_id": await repository.add_wallet(wallet_instance)}

@app.get("/wallets/{user_id}")
async def get_user_wallets(user_id: int):
    return {"wallets": await repository.get_wallets(user_id)}

@app.post("/categories")
async def create_user_category(payload: CategoryCreate):
    category_instance = Category(
        category_id=0,
        user_id=payload.user_id,
        name=payload.name,
        category_type=payload.category_type,
        icon=payload.icon
    )
    return {"category_id": await repository.add_category(category_instance)}

@app.get("/categories/{user_id}/{category_type}")
async def get_user_categories(user_id: int, category_type: str):
    return {"categories": await repository.get_categories(user_id, category_type)}