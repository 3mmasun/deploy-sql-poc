# Deployment Overview

## Deployment Information

- **Environment**: prod
- **Deployment Week**: 2026-w15
- **Generated**: 2026-04-07 15:06:02
- **Total Scripts**: 6

## Deployment Scripts

### 1. scripts/schema/01_create_users_table.sql

**JIRA Issue**: DATA-101
**Author**: Alice Johnson
**Impact**: Creates users table with 5 columns (id, username, email, created_at, updated_at)

### 2. scripts/schema/02_create_orders_table.sql

**JIRA Issue**: DATA-102
**Author**: Bob Smith
**Impact**: Creates orders table with 5 columns and FK to users (1:N relationship)

### 3. scripts/operations/01_insert_sample_users.sql

**JIRA Issue**: DATA-201
**Author**: Charlie Davis
**Impact**: Inserts 3 new user records into users table

### 4. scripts/operations/02_insert_sample_orders.sql

**JIRA Issue**: DATA-202
**Author**: Elena White
**Impact**: Inserts 4 new order records totaling $725.75 in sales

### 5. scripts/others/01_create_role.sql

**JIRA Issue**: DATA-301
**Author**: Frank Miller
**Impact**: Creates data_analyst role with SELECT permissions on all tables in public schema

### 6. scripts/others/02_create_views.sql

**JIRA Issue**: DATA-302
**Author**: Grace Lee
**Impact**: Creates order_summary view aggregating order counts and totals per user (3 users)
