-- ============================================================================
-- Metadata
-- ============================================================================
-- JIRA Issue: DATA-202
-- Author: Elena White
-- Impact: Inserts 4 new order records totaling $725.75 in sales
-- ============================================================================

-- Insert sample orders
INSERT INTO orders (order_id, user_id, total_amount, status) VALUES
(101, 1, 150.50, 'COMPLETED'),
(102, 2, 200.00, 'COMPLETED'),
(103, 1, 75.25, 'PENDING'),
(104, 3, 300.00, 'COMPLETED');
