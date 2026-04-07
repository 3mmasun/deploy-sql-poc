-- ============================================================================
-- Metadata
-- ============================================================================
-- JIRA Issue: DATA-201
-- Author: Charlie Davis
-- Impact: Inserts 3 new user records into users table
-- ============================================================================

-- Insert sample users
INSERT INTO users (user_id, username, email) VALUES
(1, 'john_doe', 'john@example.com'),
(2, 'jane_smith', 'jane@example.com'),
(3, 'bob_wilson', 'bob@example.com');
