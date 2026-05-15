# SQL Pre-Commit Testing with Optim Test Data

A simple demonstration of how test data catches SQL bugs **before** they reach production.

## Quick Start

### 1. Run the tests (they should all pass)
```bash
cd TDM/mock_app
python3 test_sql.py
```

**Expected output:**
```
✅ All 8 tests PASSED
✅ Your SQL queries are validated with test data
✅ Safe to commit your changes
```

### 2. Try breaking something!

Edit [`credit_risk_queries.sql`](credit_risk_queries.sql) and introduce a bug:

**Example 1: Typo in column name**
```sql
-- Change this:
SELECT loan_amount FROM credit_applications

-- To this (typo):
SELECT loan_amout FROM credit_applications
```

**Example 2: Wrong data value**
```sql
-- Change this:
WHERE risk = 'Risk'

-- To this (wrong value):
WHERE risk = 'High Risk'
```

**Example 3: Remove NULL protection**
```sql
-- Change this:
COALESCE(employment_duration, 'Unknown')

-- To this (no NULL handling):
employment_duration
```

### 3. Run tests again
```bash
python3 test_sql.py
```

**Expected output:**
```
❌ TESTS FAILED!
⚠️  DO NOT COMMIT - Breaking changes detected!
```

The tests will show you exactly what's wrong and prevent you from committing broken SQL!

## What Gets Tested

| Test | What It Catches | Example Bug |
|------|----------------|-------------|
| **Column Names** | Typos in column names | `loan_amout` instead of `loan_amount` |
| **Data Values** | Wrong values in WHERE clauses | `'High Risk'` when data has `'Risk'` |
| **Division by Zero** | Unsafe calculations | `COUNT(*) = 0` causing division error |
| **NULL Handling** | Missing NULL checks | NULL values breaking GROUP BY |
| **Data Types** | Type mismatches | `age < '25'` (string) vs `age < 25` (int) |
| **Aggregations** | Wrong calculations | Incorrect percentage formulas |
| **CASE Logic** | Wrong ordering | Age groups misclassified |
| **Output Structure** | Missing columns | Downstream code breaks |

## Why This Matters

### ❌ Without Test Data
```
Developer writes SQL → Commits → Deploys → Production crashes → Emergency fix
```

**Problems:**
- Bugs discovered by customers
- Production downtime
- Emergency hotfixes
- Lost revenue

### ✅ With Test Data
```
Developer writes SQL → Tests run → Bug caught → Fix before commit → Deploy safely
```

**Benefits:**
- Bugs caught in seconds
- No production issues
- Confident deployments
- Happy customers

## Real-World Example

**Scenario:** You write this query:
```sql
SELECT AVG(loan_amount) / COUNT(*)
FROM credit_applications
WHERE employment_duration = 'unemployed';
```

**Without test data:**
- Looks fine in your editor
- Passes code review
- Deploys to production
- **CRASHES** when no unemployed applicants exist (division by zero)
- Customer sees error page
- Emergency fix required

**With test data:**
- Test runs against 500 synthetic records
- Discovers `'unemployed'` returns 0 rows
- Catches division by zero **before commit**
- You fix it immediately
- Never reaches production

## Files

- **[`credit_risk_queries.sql`](credit_risk_queries.sql)** - SQL queries with inline documentation of common mistakes
- **[`test_sql.py`](test_sql.py)** - Test suite that validates queries against test data
- **[`credit_risk_mock_data.csv`](credit_risk_mock_data.csv)** - Synthetic test data (500 records)

## Try It Yourself

1. **Make a breaking change** in [`credit_risk_queries.sql`](credit_risk_queries.sql)
2. **Run tests**: `python3 test_sql.py`
3. **See it fail** with clear error message
4. **Fix the bug**
5. **Run tests again** - they pass!
6. **Commit with confidence**

## Integration with Git Hooks

You can set up a pre-commit hook to automatically run these tests:

```bash
# In .git/hooks/pre-commit
if git diff --cached --name-only | grep -q "credit_risk_queries.sql"; then
    cd TDM/mock_app && python3 test_sql.py || exit 1
fi
```

Now tests run automatically whenever you commit changes to the SQL file!

---

**Made with Bob** 🤖
