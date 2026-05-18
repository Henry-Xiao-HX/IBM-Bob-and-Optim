# Credit Risk Assessment Mock App

This directory contains a focused IBM Optim TDM mock application for validating application and SQL changes with synthetic credit-risk data.

## What is here

- **[`credit_risk_queries.sql`](credit_risk_queries.sql)** - SQL queries used by the demo and SQL tests
- **[`test_sql.py`](test_sql.py)** - SQL validation tests against synthetic/mock data
- **[`credit_risk_mock_data.csv`](credit_risk_mock_data.csv)** - Local fallback dataset for offline validation
- **[`run_tests.sh`](run_tests.sh)** - Helper script for running the test workflow
- **[`setup_git_hook.sh`](setup_git_hook.sh)** - Installs the local Git pre-commit hook
- **[`git-hooks/pre_commit_test_app_tdm`](git-hooks/pre_commit_test_app_tdm)** - Versioned hook source

## Relationship to the main TDM guide

Use the top-level [`TDM/README.md`](../README.md) for:
- IBM Optim TDM concepts
- synthetic data generation workflow
- masking and compliance overview
- CI/CD patterns across teams

Use this README for:
- the credit risk mock app
- local test execution
- SQL validation workflow
- pre-commit hook setup for this directory

## Quick start

From [`TDM/mock_app`](README.md):

```bash
pip install -r ../../requirements.txt
./run_tests.sh
```

If you want hook-based validation on commit:

```bash
./setup_git_hook.sh
```

## Configuration

Create a repository-level [`.env`](../../.env.example) based on [`.env.example`](../../.env.example) and provide your Optim credentials:

```bash
OPTIM_BASE_URL=https://your-optim-server:7725/optim
OPTIM_USERNAME=your_username
OPTIM_PASSWORD=your_password
OPTIM_ACCOUNT_ID=your_account_id
```

If Optim is unavailable, the tests fall back to [`credit_risk_mock_data.csv`](credit_risk_mock_data.csv).

## Test workflows

### 1. Run the standard mock app test flow

```bash
./run_tests.sh
```

This flow is intended to validate the mock application against fresh synthetic data when Optim is reachable, or the local CSV fallback when it is not.

### 2. Run the SQL-focused validation flow

```bash
python3 test_sql.py
```

Expected success output:

```text
✅ All 8 tests PASSED
✅ Your SQL queries are validated with test data
✅ Safe to commit your changes
```

## SQL validation workflow

The SQL workflow demonstrates how test data catches query bugs before they reach production.

### Try breaking a query

Edit [`credit_risk_queries.sql`](credit_risk_queries.sql) and introduce a bug.

**Example: typo in a column name**
```sql
SELECT loan_amout FROM credit_applications
```

**Example: wrong filter value**
```sql
WHERE risk = 'High Risk'
```

**Example: remove NULL protection**
```sql
employment_duration
```

Then rerun:

```bash
python3 test_sql.py
```

Expected failure output:

```text
❌ TESTS FAILED!
⚠️  DO NOT COMMIT - Breaking changes detected!
```

### What the SQL tests catch

| Test Area | What It Catches | Example |
|-----------|------------------|---------|
| Column names | Typos in selected or filtered fields | `loan_amout` vs `loan_amount` |
| Data values | Invalid literals in filters | `'High Risk'` vs expected values |
| Division safety | Unsafe math on empty result sets | divide-by-zero scenarios |
| NULL handling | Missing `COALESCE` or similar guards | nullable employment fields |
| Data types | Incorrect comparisons or casting assumptions | string vs numeric comparisons |
| Aggregations | Broken percentages and totals | wrong AVG / COUNT logic |
| CASE logic | Misordered business rules | incorrect risk grouping |
| Output shape | Missing or renamed columns | downstream consumer failures |

## Pre-commit hook workflow

This directory includes a local hook installer for running validation before commit.

### Install

```bash
./setup_git_hook.sh
```

### What it does

1. Detects relevant staged changes
2. Runs the test workflow
3. Blocks the commit if tests fail
4. Allows the commit if validation passes

### Manual validation before commit

```bash
./run_tests.sh
python3 test_sql.py
```

### Bypass only in emergencies

```bash
git commit --no-verify -m "Emergency fix"
```

## Why this demo matters

### Without test data

```text
Developer writes SQL → Commits → Deploys → Production issue → Emergency fix
```

### With synthetic test data

```text
Developer writes SQL → Tests run locally → Bug caught → Fix before commit
```

Benefits:
- faster feedback
- privacy-safe validation
- fewer production regressions
- more confident commits

## Troubleshooting

### Missing Optim configuration

Create the repository-level [`.env`](../../.env.example) with valid credentials.

### Authentication failures

Verify `OPTIM_BASE_URL`, `OPTIM_USERNAME`, and `OPTIM_PASSWORD`.

### No archive jobs found

Confirm Optim Archive has at least one usable archive job and the account has access.

### Tests fall back to CSV

This is expected when:
- the [`.env`](../../.env.example) file is missing
- Optim is unavailable
- network access is blocked

## References

- Main TDM guide: [`TDM/README.md`](../README.md)
- Project root guide: [`README.md`](../../README.md)
- API docs: [`docs/optim-tdm-1.1.0_api-docs.yaml`](../../docs/optim-tdm-1.1.0_api-docs.yaml)