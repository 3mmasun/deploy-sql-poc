-- ============================================================================
-- Metadata
-- ============================================================================
-- JIRA Issue: DATA-101
-- Author: Alice Johnson
-- Impact: Creates users table with 5 columns (id, username, email, created_at, updated_at)
-- ============================================================================

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
