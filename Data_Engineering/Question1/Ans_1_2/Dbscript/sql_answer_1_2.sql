BEGIN;

    CREATE SCHEMA IF NOT EXISTS data_engineering_1_2;

    CREATE TABLE data_engineering_1_2.customers (
        customer_id VARCHAR(100) PRIMARY KEY,
        name VARCHAR(300) NOT NULL
    );

    CREATE TABLE data_engineering_1_2.merchants (
        merchant_id VARCHAR(100) PRIMARY KEY,
        merchant_name VARCHAR(300) NOT NULL,
        type VARCHAR(100) NOT NULL,
        date DATE NOT NULL
    );

    CREATE TABLE data_engineering_1_2.promotions (
        promotion_id INTEGER PRIMARY KEY,
        promotion_name VARCHAR(300) NOT NULL,
        merchant_id VARCHAR(100) NOT NULL,
        req_point INTEGER NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        CONSTRAINT fk_promo_merchant FOREIGN KEY (merchant_id) 
            REFERENCES data_engineering_1_2.merchants (merchant_id)
    );

    CREATE TABLE data_engineering_1_2.cc_transactions (
        transaction_id VARCHAR(100) PRIMARY KEY,
        customer_id VARCHAR(100) NOT NULL,
        credit_card_number VARCHAR(20) NOT NULL,
        transaction_date DATE NOT NULL,
        merchant_id VARCHAR(100) NOT NULL,
        transaction_amount FLOAT NOT NULL,
        CONSTRAINT fk_txn_customer FOREIGN KEY (customer_id) 
            REFERENCES data_engineering_1_2.customers (customer_id),
        CONSTRAINT fk_txn_merchant FOREIGN KEY (merchant_id) 
            REFERENCES data_engineering_1_2.merchants (merchant_id)
    );

    CREATE TABLE data_engineering_1_2.point_balance (
        customer_id VARCHAR(100) NOT NULL,
        point_balance_date DATE NOT NULL,
        point_balance INTEGER NOT NULL,
        CONSTRAINT pk_point_balance_1_2 PRIMARY KEY (customer_id, point_balance_date),
        CONSTRAINT fk_point_customer FOREIGN KEY (customer_id) 
            REFERENCES data_engineering_1_2.customers (customer_id)
    );

COMMIT;