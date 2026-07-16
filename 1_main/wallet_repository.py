from asyncpg import connect



class AsyncTransactionRepository:
    def __init__(self, db_config):
        self.__db_config = db_config

    async def add_transaction(self, transaction):
        connection = await connect(**self.__db_config)
        try:
            transaction_id = await connection.fetchval("INSERT INTO transactions (user_id, amount, category, description) VALUES ($1, $2, $3, $4) RETURNING id", transaction.user_id, transaction.amount, transaction.category, transaction.description)
            return transaction_id
        finally:
            await connection.close()
            
    async def delete_transaction(self, transaction_id):
        connection = await connect(**self.__db_config)
        try:
            await connection.execute("DELETE FROM transactions WHERE id = $1", transaction_id)
        finally:
            await connection.close()
    
    async def get_user_transaction(self, user_id):
        connection = await connect(**self.__db_config)
        try:
            return await connection.fetch("SELECT * FROM transactions WHERE user_id = $1", user_id)
        finally:
            await connection.close()