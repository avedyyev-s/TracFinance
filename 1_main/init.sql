CREATE TABLE IF NOT EXISTS transactions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NULL,
    amount INT NULL,
    category VARCHAR(100) NOT NULL,
    description TEXT
);
