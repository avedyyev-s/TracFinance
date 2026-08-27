from asyncpg import connect

class AsyncTransactionRepository:
    def __init__(self, db_config):
        self.__db_config = db_config

    async def add_transaction(self, transaction):
        connection = await connect(**self.__db_config)
        try:
            transaction_id = await connection.fetchval("INSERT INTO transactions (user_id, wallet_id, category_id, transaction_type, amount, description) VALUES ($1, $2, $3, $4, $5, $6) RETURNING id", transaction.user_id, transaction.wallet_id, transaction.category_id, transaction.transaction_type, transaction.amount, transaction.description)
            if transaction.transaction_type == "income":
                await connection.execute("UPDATE wallets SET balance = balance + $1 WHERE id = $2", transaction.amount, transaction.wallet_id)
            else:
                await connection.execute("UPDATE wallets SET balance = balance - $1 WHERE id = $2", transaction.amount, transaction.wallet_id)
            return transaction_id  
        finally:
            await connection.close()
            
    async def delete_transaction(self, transaction_id):
        connection = await connect(**self.__db_config)
        try:
            await connection.execute("DELETE FROM transactions WHERE id = $1", transaction_id)
        finally:
            await connection.close()
    
    async def get_transactions(self, user_id):
        connection = await connect(**self.__db_config)
        try:
            return await connection.fetch("SELECT transactions.*, categories.name AS category_name, categories.icon AS category_icon, wallets.name AS wallet_name FROM transactions LEFT JOIN categories ON transactions.category_id = categories.id LEFT JOIN wallets ON transactions.wallet_id = wallets.id WHERE transactions.user_id = $1 ORDER BY transactions.id DESC", user_id)
        finally:
            await connection.close()

    async def add_wallet(self, wallet):
        connection = await connect(**self.__db_config)
        try:
            return await connection.fetchval("INSERT INTO wallets (user_id, name, balance) VALUES ($1, $2, $3) RETURNING id", wallet.user_id, wallet.name, wallet.balance)
        finally:
            await connection.close()

    async def get_wallets(self, user_id):
        connection = await connect(**self.__db_config)
        try:
            return await connection.fetch("SELECT * FROM wallets WHERE user_id = $1", user_id)
        finally:
            await connection.close()

    async def add_category(self, category):
        connection = await connect(**self.__db_config)
        try:
            return await connection.fetchval("INSERT INTO categories (user_id, name, category_type, icon) VALUES ($1, $2, $3, $4) RETURNING id", category.user_id, category.name, category.category_type, category.icon)
        finally:
            await connection.close()

    async def get_categories(self, user_id, category_type):
        connection = await connect(**self.__db_config)
        try:
            return await connection.fetch("SELECT categories.id, categories.user_id, categories.name, categories.category_type, categories.icon, COALESCE(SUM(transactions.amount), 0) AS amount FROM categories LEFT JOIN transactions ON categories.id = transactions.category_id WHERE categories.user_id = $1 AND categories.category_type = $2 GROUP BY categories.id", user_id, category_type)
        finally:
            await connection.close()