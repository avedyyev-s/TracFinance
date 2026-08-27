CREATE TABLE IF NOT EXISTS transactions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NULL,
    wallet_id BIGINT NULL,
    category_id BIGINT NULL,
    transaction_type VARCHAR(100) NOT NULL,
    amount NUMERIC DEFAULT 0,
    transaction_date TIMESTAMPTZ DEFAULT NOW(),
    description TEXT
);


CREATE TABLE IF NOT EXISTS wallets (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NULL,
    name VARCHAR(100) NOT NULL,
    balance NUMERIC DEFAULT 0
);

CREATE TABLE IF NOT EXISTS categories (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NULL,
    name VARCHAR(100) NOT NULL,
    category_type VARCHAR(50) NOT NULL,
    icon VARCHAR(50) DEFAULT '🏷️'
);
