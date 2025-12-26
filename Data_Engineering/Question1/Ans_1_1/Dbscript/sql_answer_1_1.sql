BEGIN;

    CREATE SCHEMA IF NOT EXISTS data_engineering_1_1;

    CREATE TABLE data_engineering_1_1.customers (
        customer_id VARCHAR(100) PRIMARY KEY,
        name VARCHAR(300) NOT NULL
    );

    CREATE TABLE data_engineering_1_1.promotions (
        promotion_id INTEGER PRIMARY KEY,
        promotion_name VARCHAR(300) NOT NULL,
        merchant_id VARCHAR(100) NOT NULL,
        req_point INTEGER NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL
    );

    CREATE TABLE data_engineering_1_1.cc_transactions (
        transaction_id VARCHAR(100) PRIMARY KEY,
        customer_id VARCHAR(100) NOT NULL,
        credit_card_number VARCHAR(20) NOT NULL,
        transaction_date DATE NOT NULL,
        merchant_id VARCHAR(100) NOT NULL,
        transaction_amount FLOAT NOT NULL,
        CONSTRAINT fk_txn_customer FOREIGN KEY (customer_id) 
            REFERENCES data_engineering_1_1.customers (customer_id)
    );

    CREATE TABLE data_engineering_1_1.point_balance (
        customer_id VARCHAR(100) NOT NULL,
        point_balance_date DATE NOT NULL,
        point_balance INTEGER NOT NULL,
        CONSTRAINT pk_point_balance PRIMARY KEY (customer_id, point_balance_date),
        CONSTRAINT fk_point_customer FOREIGN KEY (customer_id) 
            REFERENCES data_engineering_1_1.customers (customer_id)
    );
COMMIT;