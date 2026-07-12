from asyncpg import connect



class AsyncTransactionRepository:
    def __init__(self, db_config):
        self.__db_config = db_config

    async def add_transaction(self, transaction):
        async with connect(**self.__db_config) as connection:
            transaction_id = await connection.fetchval("INSERT INTO transactions (user_id, amount, category, description) VALUES ($1, $2, $3, $4) RETURNING id", transaction.user_id, transaction.amount, transaction.category, transaction.description)
        return transaction_id
            
    async def delete_transaction(self, transaction_id):
        async with connect(**self.__db_config) as connection:
            await connection.execute("DELETE FROM transactions WHERE id = $1", transaction_id)
    
    async def get_user_transaction(self, user_id):
        async with connect(**self.__db_config) as connection:
            return await connection.fetch("SELECT * FROM transactions WHERE user_id = $1", user_id)