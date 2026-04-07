-- ============================================================================
-- Metadata
-- ============================================================================
-- JIRA Issue: DATA-301
-- Author: Frank Miller
-- Impact: Creates data_analyst role with SELECT permissions on all tables in public schema
-- ============================================================================

-- Create role for data access
CREATE ROLE IF NOT EXISTS data_analyst;

-- Grant privileges
GRANT USAGE ON SCHEMA public TO ROLE data_analyst;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO ROLE data_analyst;
