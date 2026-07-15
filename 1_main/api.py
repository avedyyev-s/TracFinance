from fastapi import FastAPI
from pydantic import BaseModel
from models import Transaction
from main import repository

app = FastAPI()

class TransactionCreate(BaseModel):
    user_id: int
    amount: float
    category: str
    description: str

@app.post("/transactions")
async def creat_transaction(payload: TransactionCreate):
    transaction_instance = Transaction(
        transaction_id=0,
        user_id=payload.user_id,
        amount=payload.amount,
        category=payload.category,
        description=payload.description
    )
    creat_transaction_id = await repository.add_transaction(transaction_instance)

    return {"transaction_id": creat_transaction_id}

@app.get("/transactions/{user_id}")
async def get_transactions_history(user_id: int):
    transactions_history = await repository.get_user_transaction(user_id)
    return {"transaction_history": transactions_history}

@app.delete("/transactions/{transaction_id}")
async def del_transaction(transaction_id: int):
    transaction_delete = await repository.delete_transaction(transaction_id)
    return {"delete_transaction": "successfully deleted"}