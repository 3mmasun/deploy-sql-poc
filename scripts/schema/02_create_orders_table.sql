-- ============================================================================
-- Metadata
-- ============================================================================
-- JIRA Issue: DATA-102
-- Author: Bob Smith
-- Impact: Creates orders table with 5 columns and FK to users (1:N relationship)
-- ============================================================================

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    total_amount DECIMAL(10, 2),
    status VARCHAR(50) DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
