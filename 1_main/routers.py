from fastapi import APIRouter, FastAPI
from wallet_repository import AsyncTransactionRepository

router = APIRouter()

@router.post("/transactions")
async def create_transaction_endpoint():
    pass