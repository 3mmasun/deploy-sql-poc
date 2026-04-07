-- ============================================================================
-- Metadata
-- ============================================================================
-- JIRA Issue: DATA-302
-- Author: Grace Lee
-- Impact: Creates order_summary view aggregating order counts and totals per user (3 users)
-- ============================================================================

-- Create view for order summary
CREATE OR REPLACE VIEW order_summary AS
SELECT
    u.user_id,
    u.username,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_spent
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.username;
