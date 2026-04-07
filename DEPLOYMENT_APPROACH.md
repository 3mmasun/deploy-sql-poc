# SQL Deployment POC

## Implementation Approach

This proof of concept demonstrates a scalable, conflict-resistant approach to managing SQL script deployments across multiple environments.

### Folder Structure

#### Assumptions
Non-prod testing can be done on feature branch since the same set of of files will be tested across all environment. 

Therefore, `dev` `uat` and `preprod` will all read from deployment/non-prod folder

```
deployment/
├── non-prod/
│   ├── simon-deployment.yaml    (Engineer Simon)
└── prod/
    └── 2026-w15/
        ├── bob-deployment.yaml    (Engineer Bob)
        └── alice-deployment.yaml  (Engineer Alice)

scripts/
├── schema/
│   ├── 01_create_users_table.sql
│   └── 02_create_orders_table.sql
├── operations/
│   ├── 01_insert_sample_users.sql
│   └── 02_insert_sample_orders.sql
└── others/
    ├── 01_create_role.sql
    └── 02_create_views.sql
```

### Deployment Process

1. **Multiple YAML files** in the same deployment folder represent different engineers' work
2. **deploy.py script** reads all YAML files, combines them in sorted order
3. **Generates two artifacts**:
   - `deploy_overview.md` - Markdown review document with metadata
   - `scripts/2_scripts` - Ordered script list for deployment tools
4. **CICD**: subsequent steps can rely on the artifacts produced for approver review or actual deployment

## Key Benefits

### 1. **Avoids Merge Conflicts**

**Traditional Approach (Conflict-Prone):**

deployment.yaml represents a file that every engineer must modify to get their scripts deployed in an environment.

```
main branch
    ↑
    ├─ feature/JIRA-101 (modifies: deployment.yaml)
    │   └─ Adds schema scripts
    │
    └─ feature/JIRA-202 (modifies: deployment.yaml)
        └─ Adds operations scripts

    ❌ CONFLICT: Both branches modify the same file
```

**New Approach (Conflict-Free):**
Folder based, different files
`
```
main branch
    ↑
    ├─ feature/JIRA-101 (creates: deployment/prod/<DEPLOY_ID>/bob-deployment.yaml)
    │   └─ New file, no conflicts
    │
    └─ feature/JIRA-202 (creates: deployment/prod/<DEPLOY_ID>/alice-deployment.yaml)
        └─ New file, no conflicts

    ✅ Merge cleanly: Different files in same directory
```

deployment.yaml is a list of SQL scripts to run in sequence.
```
scripts:
  - scripts/schema/01_create_users_table.sql
  - scripts/schema/02_create_orders_table.sql
```

SQL script metadata (recommended)
```
-- ============================================================================
-- Metadata
-- ============================================================================
-- JIRA Issue: DATA-301
-- Author: Frank Miller
-- Impact: Creates data_analyst role with SELECT permissions on all tables in public schema
-- ============================================================================
```

**Why This Works:**
- Each engineer creates their own YAML file (e.g., `bob-deployment.yaml`, `alice-deployment.yaml`)
- Git naturally merges different files without conflicts
- The deploy script combines them automatically

### 2. **Complete Deployment History in Main**

All historical deployments are kepted in `deployment/prod/<DEPLOY_ID>`

### 3. **Clear Metadata for Reviewers**

Each SQL script includes metadata:
```sql
-- JIRA Issue: DATA-101
-- Author: Alice Johnson
-- Impact: Creates users table with 5 columns (id, username, email, created_at, updated_at)
```

Generated `deploy_overview.md` provides:
- Sequential list of all scripts being deployed
- JIRA issue tracking
- Engineer/author accountability
- Database impact summary
- Easy to review before deployment

### 4. **Separation of Concerns**

- **SQL Scripts** (`scripts/` folder): Source of truth for database changes
- **Deployment Configs** (`deployment/` folder): Which scripts run in which environments
- **Artifacts** (`deploy_overview.md`, `2_deploy_scripts.mst`): Generated for reviewers and deployment tools

## Workflow Example

### Engineer 1: Schema Changes (JIRA-101)

```bash
# Create feature branch
git checkout -b feature/JIRA-101-add-users-table

# Create SQL script
# scripts/schema/01_create_users_table.sql

# Create new YAML file for non-prod deployment and test in lower environments
# deployment/non-prod/bob-deployment.yaml

# Move YAML file into prod deployment
# deployment/prod/2026-w15/bob-deployment.yaml

# Commit changes
# Create pull request to main
```

### Engineer 2: Operations (JIRA-202)

```bash
# Create independent feature branch
git checkout -b feature/JIRA-202-add-order-operations

# Create SQL scripts
# scripts/operations/01_insert_sample_orders.sql

# Create different YAML file (different naming) and test in lower environment
# deployment/non-prod/alice-deployment.yaml

# Move YAML file into prod deployment
# deployment/prod/2026-w15/alice-deployment.yaml

# Commit changes
# Create pull request to main
```

## Deployment Environments

```bash
# Non-prod (dev, uat, preprod all use same scripts)
python3 deploy.py dev       → uses deployment/non-prod/
python3 deploy.py uat       → uses deployment/non-prod/
python3 deploy.py preprod   → uses deployment/non-prod/

# Production (explicit week parameter required)
python3 deploy.py prod 2026-w15      → uses deployment/prod/2026-w15/
python3 deploy.py prod 2026-w16      → uses deployment/prod/2026-w16/
```

## Summary

| Aspect | Benefit |
|--------|---------|
| **Merge Conflicts** | ✅ Eliminated through separate YAML files |
| **History** | ✅ Complete deployment kept in explicit `prod/<DEPLOY_ID>` folder |
| **Scalability** | ✅ Supports unlimited concurrent deployments |
| **Automation** | ✅ Auto-generated review documents |
