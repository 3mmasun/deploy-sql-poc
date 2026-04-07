# Snowflake SQL Deployment POC

## Implementation Approach

This proof of concept demonstrates a scalable, conflict-resistant approach to managing SQL script deployments for Snowflake across multiple environments.

### Architecture

```
deployment/
├── non-prod/
│   ├── deployment-001.yaml    (Engineer 1: Schema changes)
│   ├── deployment-002.yaml    (Engineer 2: Operations)
│   └── deployment-003.yaml    (Engineer 3: Full deployment)
└── prod/
    └── 2026-w15/
        ├── deployment-1-schema.yaml    (Engineer A: Schema)
        └── deployment-2-ops.yaml       (Engineer B: Operations)

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
4. **Commits both artifacts** to main branch along with deployment YAML files

## Key Benefits

### 1. **Avoids Merge Conflicts**

**Traditional Approach (Conflict-Prone):**
```
main branch
    ↑
    ├─ feature/JIRA-101 (modifies: deployment-prod.yaml)
    │   └─ Adds schema scripts
    │
    └─ feature/JIRA-202 (modifies: deployment-prod.yaml)
        └─ Adds operations scripts

    ❌ CONFLICT: Both branches modify the same file
```

**Our Approach (Conflict-Free):**
```
main branch
    ↑
    ├─ feature/JIRA-101 (creates: deployment-1-schema.yaml)
    │   └─ New file, no conflicts
    │
    └─ feature/JIRA-202 (creates: deployment-2-ops.yaml)
        └─ New file, no conflicts

    ✅ Merge cleanly: Different files in same directory
```

**Why This Works:**
- Each engineer creates their own YAML file (e.g., `deployment-1-*.yaml`, `deployment-2-*.yaml`)
- Git naturally merges different files without conflicts
- Files are sorted alphabetically for deterministic ordering
- The deploy script combines them automatically

### 2. **Complete Deployment History in Main**

All deployment artifacts are committed to the main branch:

```bash
git log --oneline

e3f8c2e deployment: Add order operations to 2026-w15
  - deployment/prod/2026-w15/deployment-2-ops.yaml
  - deploy_overview.md (auto-generated)
  - scripts/2_deploy_scripts.mst (auto-generated)

d1a5f9b deployment: Add user schema to 2026-w15
  - deployment/prod/2026-w15/deployment-1-schema.yaml
  - deploy_overview.md (auto-generated)
  - scripts/2_deploy_scripts.mst (auto-generated)
```

**Benefits:**
- Audit trail: See exactly what was deployed in each commit
- Rollback support: Can revert to any previous deployment
- Review history: View metadata (JIRA, Author, Impact) in markdown
- Reproducible: deploy_overview.md shows exact deployment details

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

# Create new YAML file for prod deployment
# deployment/prod/2026-w15/deployment-1-schema.yaml

# Create SQL script
# scripts/schema/01_create_users_table.sql

# Run deploy script to validate
python3 deploy.py prod 2026-w15

# Review generated deploy_overview.md
# Commit changes
git add .
git commit -m "feat: Add user schema to 2026-w15 deployment (JIRA-101)"
git push origin feature/JIRA-101-add-users-table
```

### Engineer 2: Operations (JIRA-202)

```bash
# Create independent feature branch
git checkout -b feature/JIRA-202-add-order-operations

# Create different YAML file (different naming)
# deployment/prod/2026-w15/deployment-2-ops.yaml

# Create SQL scripts
# scripts/operations/01_insert_sample_orders.sql

# Run deploy script to validate
python3 deploy.py prod 2026-w15

# Commit changes
git add .
git commit -m "feat: Add order operations to 2026-w15 deployment (JIRA-202)"
git push origin feature/JIRA-202-add-order-operations
```

### Pull Requests and Merge

Both PRs merge to main **without conflicts** because:
- Different YAML files (`deployment-1-*.yaml` vs `deployment-2-*.yaml`)
- Same SQL scripts folder (no conflicts in well-organized structure)
- Auto-generated artifacts (`deploy_overview.md`, `2_deploy_scripts.mst`) refresh on merge

Result in main branch:
```
deployment/prod/2026-w15/
├── deployment-1-schema.yaml       (from JIRA-101)
├── deployment-2-ops.yaml          (from JIRA-202)
deploy_overview.md                 (combined, latest)
scripts/2_deploy_scripts.mst        (combined, latest)
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
| **History** | ✅ Complete audit trail in git log |
| **Traceability** | ✅ JIRA + Author + Impact metadata |
| **Scalability** | ✅ Supports unlimited concurrent deployments |
| **Safety** | ✅ Explicit week parameter for prod deployments |
| **Automation** | ✅ Auto-generated review documents |

This approach enables teams to work in parallel, ship faster, and maintain a complete history of all database deployments.
