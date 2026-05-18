-- ============================================================
-- MoMo SMS Data Processing System
-- Database Setup Script (MySQL)
-- Team Alpha
-- ============================================================
-- This script creates the full database schema, inserts sample
-- data, and builds indexes for performance.
-- Run order: DROP tables -> CREATE TABLEs -> INSERT data -> CREATE INDEXes
-- The script is safe to re-run: it drops existing tables first.
-- ============================================================


-- ============================================================
-- SECTION 0: CLEAN SLATE
-- Drop existing tables in reverse dependency order so the
-- script can be run repeatedly without "table already exists"
-- errors. IF EXISTS makes this safe even on the first run.
-- ============================================================
DROP TABLE IF EXISTS system_logs;
DROP TABLE IF EXISTS transaction_participants;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS sms_messages;
DROP TABLE IF EXISTS sms_backups;
DROP TABLE IF EXISTS contacts;
DROP TABLE IF EXISTS transaction_categories;
DROP TABLE IF EXISTS users;


-- ============================================================
-- SECTION 1: TABLE CREATION (DDL)
-- Tables are created in dependency order so that any table
-- referenced by a FOREIGN KEY exists before the table that
-- points to it.
-- ============================================================

-- ---------- TABLE 1: USERS ----------
-- The MoMo account owners.
CREATE TABLE users (
    user_id INT AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL COMMENT 'Full name of the account owner',
    email VARCHAR(100) NOT NULL UNIQUE COMMENT 'Unique email address',
    phone_number VARCHAR(20) NOT NULL COMMENT 'User mobile number in international format',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation timestamp',
    PRIMARY KEY (user_id)
) ENGINE=InnoDB;

-- ---------- TABLE 2: TRANSACTION_CATEGORIES ----------
-- Lookup table for transaction types (withdrawal, payment, etc.).
CREATE TABLE transaction_categories (
    category_id INT AUTO_INCREMENT,
    category_name VARCHAR(50) NOT NULL UNIQUE COMMENT 'Name of the category',
    description TEXT COMMENT 'Description of the category',
    PRIMARY KEY (category_id)
) ENGINE=InnoDB;

-- ---------- TABLE 3: CONTACTS ----------
-- People or organizations the MoMo account owner interacts with.
CREATE TABLE contacts (
    contact_id INT AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL COMMENT 'Name of the contact',
    phone_number VARCHAR(20) NOT NULL UNIQUE COMMENT 'Contact phone number',
    reference_code VARCHAR(20) COMMENT 'Optional short code identifying the contact',
    contact_type ENUM('Person','Merchant','Company','Bank') NOT NULL COMMENT 'Type of contact',
    PRIMARY KEY (contact_id)
) ENGINE=InnoDB;

-- ---------- TABLE 4: SMS_BACKUPS ----------
-- Each backup set uploaded by a user; contains many SMS messages.
CREATE TABLE sms_backups (
    backup_id INT AUTO_INCREMENT,
    user_id INT NOT NULL,
    backup_set_uuid VARCHAR(100) UNIQUE COMMENT 'Globally unique ID for the backup set',
    backup_date DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Date the backup was made',
    backup_type VARCHAR(20) NOT NULL COMMENT 'Backup type, e.g. full or incremental',
    sms_count INT COMMENT 'Number of SMS messages in the backup',
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Upload timestamp',
    PRIMARY KEY (backup_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
) ENGINE=InnoDB;

-- ---------- TABLE 5: SMS_MESSAGES ----------
-- Each individual SMS message extracted from a backup.
CREATE TABLE sms_messages (
    sms_id INT AUTO_INCREMENT,
    backup_id INT NOT NULL,
    address VARCHAR(50) COMMENT 'Sender address of the SMS',
    body TEXT COMMENT 'Full text content of the SMS',
    readable_date DATETIME COMMENT 'Date the SMS was received',
    service_center VARCHAR(50) COMMENT 'Telecom SMS service center number',
    read_status BOOLEAN DEFAULT FALSE COMMENT 'Whether the SMS has been read',
    status INT COMMENT 'Technical status code from raw SMS data',
    protocol INT COMMENT 'Technical protocol code from raw SMS data',
    contact_name VARCHAR(100) COMMENT 'Name attached to the sender, if known',
    PRIMARY KEY (sms_id),
    FOREIGN KEY (backup_id) REFERENCES sms_backups(backup_id)
) ENGINE=InnoDB;

-- ---------- TABLE 6: TRANSACTIONS ----------
-- Core table: one mobile money transaction per row.
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT,
    sms_id INT UNIQUE COMMENT 'Source SMS (1:1 relationship)',
    category_id INT COMMENT 'Transaction category',
    transaction_ref VARCHAR(50) UNIQUE COMMENT 'Unique transaction reference',
    financial_tx_id VARCHAR(50) COMMENT 'Financial system transaction ID',
    external_tx_id VARCHAR(50) COMMENT 'External system transaction ID',
    amount DECIMAL(12,2) NOT NULL COMMENT 'Transaction amount (exact value)',
    fee DECIMAL(12,2) DEFAULT 0.00 COMMENT 'Transaction fee',
    currency CHAR(3) DEFAULT 'RWF' COMMENT 'Three-letter currency code',
    balance_after DECIMAL(12,2) COMMENT 'Account balance after the transaction',
    transaction_datetime DATETIME NOT NULL COMMENT 'When the transaction occurred',
    direction ENUM('IN','OUT') NOT NULL COMMENT 'Money in or money out',
    status VARCHAR(20) COMMENT 'Transaction status, e.g. completed, pending, failed',
    notes TEXT COMMENT 'Free-form notes',
    PRIMARY KEY (transaction_id),
    FOREIGN KEY (sms_id) REFERENCES sms_messages(sms_id),
    FOREIGN KEY (category_id) REFERENCES transaction_categories(category_id),
    CHECK (amount >= 0),
    CHECK (fee >= 0)
) ENGINE=InnoDB;

-- ---------- TABLE 7: TRANSACTION_PARTICIPANTS ----------
-- Junction table resolving the M:N relationship between
-- transactions and contacts. Each row records the role a
-- contact played in a given transaction.
CREATE TABLE transaction_participants (
    participant_id INT AUTO_INCREMENT,
    transaction_id INT NOT NULL,
    contact_id INT NOT NULL,
    role ENUM('SENDER','RECEIVER','MERCHANT','BANK') NOT NULL COMMENT 'Role of the contact in the transaction',
    PRIMARY KEY (participant_id),
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id),
    FOREIGN KEY (contact_id) REFERENCES contacts(contact_id)
) ENGINE=InnoDB;

-- ---------- TABLE 8: SYSTEM_LOGS ----------
-- Machine-generated records tracking the data processing pipeline.
-- The three foreign keys are nullable because a log entry may
-- relate to any one of them, all, or none.
CREATE TABLE system_logs (
    log_id INT AUTO_INCREMENT,
    user_id INT,
    sms_id INT,
    transaction_id INT,
    action VARCHAR(100) NOT NULL COMMENT 'Short description of the logged action',
    log_level ENUM('INFO','WARNING','ERROR') NOT NULL COMMENT 'Severity of the log entry',
    message TEXT COMMENT 'Detailed log message',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Log creation timestamp',
    PRIMARY KEY (log_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (sms_id) REFERENCES sms_messages(sms_id),
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
) ENGINE=InnoDB;


-- ============================================================
-- SECTION 2: SAMPLE DATA (DML)
-- Inserted in dependency order. Primary keys are omitted because
-- AUTO_INCREMENT generates them automatically.
-- ============================================================

-- ---------- USERS ----------
INSERT INTO users (full_name, email, phone_number) VALUES
('Alvin Mugisha',   'alvin@example.com',   '+250788100001'),
('Stacey Kanogo',   'stacey@example.com',  '+250788100002'),
('Jessica Bizima',  'jessica@example.com', '+250788100003'),
('Eric Niyonzima',  'eric@example.com',    '+250788100004'),
('Diane Uwase',     'diane@example.com',   '+250788100005');

-- ---------- TRANSACTION_CATEGORIES ----------
INSERT INTO transaction_categories (category_name, description) VALUES
('Withdrawal', 'Cash withdrawn from a MoMo agent'),
('Deposit',    'Cash deposited into a MoMo account'),
('Transfer',   'Money sent from one user to another'),
('Payment',    'Payment made to a merchant or bill'),
('Airtime',    'Airtime or bundle purchase');

-- ---------- CONTACTS ----------
INSERT INTO contacts (full_name, phone_number, reference_code, contact_type) VALUES
('John Doe',       '+250788200001', 'REF001', 'Person'),
('Kigali Market',  '+250788200002', 'REF002', 'Merchant'),
('Bank of Kigali', '+250788200003', 'REF003', 'Bank'),
('MTN Rwanda',     '+250788200004', 'REF004', 'Company'),
('Marie Claire',   '+250788200005', 'REF005', 'Person');

-- ---------- SMS_BACKUPS ----------
INSERT INTO sms_backups (user_id, backup_set_uuid, backup_type, sms_count) VALUES
(1, '550e8400-e29b-41d4-a716-446655440001', 'full',        120),
(2, '550e8400-e29b-41d4-a716-446655440002', 'incremental',  15),
(3, '550e8400-e29b-41d4-a716-446655440003', 'full',         98),
(4, '550e8400-e29b-41d4-a716-446655440004', 'full',        210),
(5, '550e8400-e29b-41d4-a716-446655440005', 'incremental',   7);

-- ---------- SMS_MESSAGES ----------
INSERT INTO sms_messages (backup_id, address, body, readable_date, service_center, read_status, status, protocol, contact_name) VALUES
(1, 'M-Money', 'You have received 5000 RWF from John Doe',   '2024-05-01 09:15:00', '+250788000000', TRUE,  0, 0, 'MoMo'),
(2, 'M-Money', 'Your payment of 12000 RWF to Kigali Market', '2024-05-02 14:30:00', '+250788000000', TRUE,  0, 0, 'MoMo'),
(3, 'M-Money', 'You have withdrawn 20000 RWF',               '2024-05-03 11:00:00', '+250788000000', FALSE, 0, 0, 'MoMo'),
(4, 'M-Money', 'Airtime purchase of 1000 RWF successful',    '2024-05-04 18:45:00', '+250788000000', TRUE,  0, 0, 'MoMo'),
(5, 'M-Money', 'You have sent 8000 RWF to Marie Claire',     '2024-05-05 07:20:00', '+250788000000', FALSE, 0, 0, 'MoMo');

-- ---------- TRANSACTIONS ----------
INSERT INTO transactions (sms_id, category_id, transaction_ref, financial_tx_id, external_tx_id, amount, fee, currency, balance_after, transaction_datetime, direction, status, notes) VALUES
(1, 2, 'TXN0001', 'FIN0001', 'EXT0001',  5000.00,   0.00, 'RWF', 25000.00, '2024-05-01 09:15:00', 'IN',  'completed', 'Received from John Doe'),
(2, 4, 'TXN0002', 'FIN0002', 'EXT0002', 12000.00, 100.00, 'RWF', 13000.00, '2024-05-02 14:30:00', 'OUT', 'completed', 'Payment to Kigali Market'),
(3, 1, 'TXN0003', 'FIN0003', 'EXT0003', 20000.00, 200.00, 'RWF',  5000.00, '2024-05-03 11:00:00', 'OUT', 'completed', 'Agent withdrawal'),
(4, 5, 'TXN0004', 'FIN0004', 'EXT0004',  1000.00,   0.00, 'RWF',  4000.00, '2024-05-04 18:45:00', 'OUT', 'completed', 'Airtime purchase'),
(5, 3, 'TXN0005', 'FIN0005', 'EXT0005',  8000.00,  50.00, 'RWF', 17000.00, '2024-05-05 07:20:00', 'OUT', 'completed', 'Sent to Marie Claire');

-- ---------- TRANSACTION_PARTICIPANTS ----------
INSERT INTO transaction_participants (transaction_id, contact_id, role) VALUES
(1, 1, 'SENDER'),
(2, 2, 'MERCHANT'),
(3, 3, 'BANK'),
(4, 4, 'MERCHANT'),
(5, 5, 'RECEIVER');

-- ---------- SYSTEM_LOGS ----------
INSERT INTO system_logs (user_id, sms_id, transaction_id, action, log_level, message) VALUES
(1, 1, 1, 'XML parsed',         'INFO',    'Transaction TXN0001 processed successfully'),
(2, 2, 2, 'XML parsed',         'INFO',    'Transaction TXN0002 processed successfully'),
(3, 3, 3, 'Validation warning', 'WARNING', 'Unusually large withdrawal amount'),
(4, 4, 4, 'XML parsed',         'INFO',    'Transaction TXN0004 processed successfully'),
(5, NULL, NULL, 'System startup','INFO',   'ETL pipeline started');


-- ============================================================
-- SECTION 3: INDEXES
-- Indexes speed up columns frequently used in WHERE filters
-- and JOIN conditions.
-- ============================================================
CREATE INDEX idx_tx_datetime  ON transactions(transaction_datetime);
CREATE INDEX idx_tx_category  ON transactions(category_id);
CREATE INDEX idx_tx_direction ON transactions(direction);
CREATE INDEX idx_sms_backup   ON sms_messages(backup_id);
CREATE INDEX idx_part_tx      ON transaction_participants(transaction_id);
CREATE INDEX idx_logs_level   ON system_logs(log_level);

-- ============================================================
-- END OF SCRIPT
-- ============================================================