CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    user_id INT NULL,
    amount INT NULL,
    category VARCHAR(100) NOT NULL,
    description TEXT
);
