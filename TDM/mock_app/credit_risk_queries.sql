-- Credit Risk Assessment SQL Queries
-- Demonstrates testing with synthetic data from Optim before committing changes
--
-- PRE-COMMIT TESTING WORKFLOW:
-- This file is monitored by a Git pre-commit hook. Whenever you commit changes to this file,
-- the test suite (test_sql.py) automatically runs with synthetic data from Optim Archive.
--
-- How it works:
-- 1. You modify this file (credit_risk_queries.sql)
-- 2. You stage changes: git add TDM/mock_app/credit_risk_queries.sql
-- 3. You commit: git commit -m "Your message"
-- 4. Pre-commit hook automatically runs test_sql.py
-- 5. If tests pass → commit proceeds
-- 6. If tests fail → commit is blocked until you fix the issues
--
-- WHY TEST DATA MATTERS:
-- Without testing with real data, these common mistakes go undetected:
--
-- ❌ BREAKING CHANGE #1: Typo in column name
--    SELECT loan_amout FROM ...  (missing 'n' in amount)
--    → Works in dev, crashes in production with "no such column" error
--
-- ❌ BREAKING CHANGE #2: Division by zero
--    SELECT 100.0 / COUNT(*) ...  (when COUNT is 0)
--    → Crashes when filtering returns no results
--
-- ❌ BREAKING CHANGE #3: Wrong data type
--    WHERE age = '25'  (string instead of integer)
--    → May work in SQLite but fails in PostgreSQL/Oracle
--
-- ❌ BREAKING CHANGE #4: Missing NULL handling
--    SELECT AVG(loan_amount) WHERE employment_duration IS NULL
--    → Returns NULL instead of 0, breaks downstream calculations
--
-- ❌ BREAKING CHANGE #5: Logic errors
--    WHERE risk = 'High Risk'  (actual value is 'Risk')
--    → Returns 0 rows, looks like no high-risk applications exist
--
-- ✅ WITH OPTIM TEST DATA:
--    - Catches these errors BEFORE commit
--    - Tests with realistic data patterns
--    - Validates queries return expected results
--    - Ensures privacy (no production data needed)

-- ============================================================================
-- SCHEMA DEFINITION
-- ============================================================================

CREATE TABLE IF NOT EXISTS credit_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    checking_status VARCHAR(50),
    loan_duration INTEGER,
    credit_history VARCHAR(50),
    loan_purpose VARCHAR(50),
    loan_amount INTEGER,
    existing_savings VARCHAR(50),
    employment_duration VARCHAR(50),
    installment_percent INTEGER,
    sex VARCHAR(10),
    others_on_loan VARCHAR(50),
    current_residence_duration INTEGER,
    owns_property VARCHAR(50),
    age INTEGER,
    installment_plans VARCHAR(50),
    housing VARCHAR(50),
    existing_credits_count INTEGER,
    job VARCHAR(50),
    dependents INTEGER,
    telephone VARCHAR(10),
    foreign_worker VARCHAR(10),
    risk VARCHAR(20)
);

-- ============================================================================
-- QUERY 1: Get High-Risk Applications
-- COMMON MISTAKE: Using wrong risk value
-- ============================================================================

-- name: get_high_risk_applications
-- ❌ BREAKING: This would return 0 rows if risk values are 'Risk' not 'High Risk'
-- ✅ FIXED: Use correct value 'Risk' from actual data
SELECT 
    id,
    loan_amount,
    loan_purpose,
    age,
    employment_duration,
    risk
FROM credit_applications
WHERE risk = 'Risk'  -- Correct value validated by test data
ORDER BY loan_amount DESC;

-- ============================================================================
-- QUERY 2: Calculate Risk Statistics
-- COMMON MISTAKE: Division by zero when no data exists
-- ============================================================================

-- name: get_risk_statistics
-- ❌ BREAKING: If COUNT(*) = 0, division causes error
-- ✅ FIXED: Use NULLIF to prevent division by zero
SELECT 
    COUNT(*) as total_applications,
    SUM(CASE WHEN risk = 'Risk' THEN 1 ELSE 0 END) as high_risk_count,
    SUM(CASE WHEN risk = 'No Risk' THEN 1 ELSE 0 END) as low_risk_count,
    ROUND(AVG(loan_amount), 2) as avg_loan_amount,
    ROUND(AVG(age), 1) as avg_age,
    -- Safe division: returns NULL instead of error when no data
    ROUND(100.0 * SUM(CASE WHEN risk = 'Risk' THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) as risk_percentage
FROM credit_applications;

-- ============================================================================
-- QUERY 3: Find Applications by Loan Purpose
-- COMMON MISTAKE: Typo in column name
-- ============================================================================

-- name: get_applications_by_purpose
-- params: loan_purpose
-- ❌ BREAKING: loan_amout (typo) would cause "no such column" error
-- ✅ FIXED: Correct spelling validated by test data
SELECT 
    id,
    loan_amount,  -- Correct spelling
    loan_purpose,
    age,
    employment_duration,
    risk
FROM credit_applications
WHERE loan_purpose = :loan_purpose
ORDER BY loan_amount DESC
LIMIT 10;

-- ============================================================================
-- QUERY 4: Young Borrowers with Large Loans (High Risk Profile)
-- COMMON MISTAKE: Wrong data type comparison
-- ============================================================================

-- name: get_young_large_loan_applications
-- ❌ BREAKING: WHERE age < '25' (string) may fail in strict databases
-- ✅ FIXED: Use integer comparison
SELECT 
    id,
    age,
    loan_amount,
    loan_purpose,
    employment_duration,
    risk
FROM credit_applications
WHERE age < 25  -- Integer comparison, not string
  AND loan_amount > 10000
ORDER BY loan_amount DESC;

-- ============================================================================
-- QUERY 5: Employment Duration Analysis
-- COMMON MISTAKE: Not handling NULL values
-- ============================================================================

-- name: analyze_risk_by_employment
-- ❌ BREAKING: NULL employment_duration creates separate group
-- ✅ FIXED: Use COALESCE to handle NULLs
SELECT 
    COALESCE(employment_duration, 'Unknown') as employment_duration,
    COUNT(*) as total_count,
    SUM(CASE WHEN risk = 'Risk' THEN 1 ELSE 0 END) as high_risk_count,
    ROUND(100.0 * SUM(CASE WHEN risk = 'Risk' THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) as risk_percentage,
    ROUND(AVG(loan_amount), 2) as avg_loan_amount
FROM credit_applications
GROUP BY COALESCE(employment_duration, 'Unknown')
ORDER BY risk_percentage DESC;

-- ============================================================================
-- QUERY 6: Loan Purpose Risk Analysis
-- COMMON MISTAKE: Incorrect aggregation logic
-- ============================================================================

-- name: analyze_risk_by_purpose
-- ❌ BREAKING: Forgetting HAVING clause returns too many small groups
-- ✅ FIXED: Filter groups with minimum count
SELECT 
    loan_purpose,
    COUNT(*) as total_count,
    SUM(CASE WHEN risk = 'Risk' THEN 1 ELSE 0 END) as high_risk_count,
    ROUND(100.0 * SUM(CASE WHEN risk = 'Risk' THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) as risk_percentage,
    ROUND(AVG(loan_amount), 2) as avg_loan_amount
FROM credit_applications
GROUP BY loan_purpose
HAVING COUNT(*) >= 5  -- Only show purposes with enough data
ORDER BY risk_percentage DESC;

-- ============================================================================
-- QUERY 7: Age Group Risk Distribution
-- COMMON MISTAKE: Incorrect CASE statement ordering
-- ============================================================================

-- name: analyze_risk_by_age_group
-- ❌ BREAKING: Wrong CASE order causes misclassification
-- ✅ FIXED: Proper ordering from smallest to largest
SELECT 
    CASE 
        WHEN age < 25 THEN 'Under 25'
        WHEN age < 35 THEN '25-34'
        WHEN age < 45 THEN '35-44'
        WHEN age < 55 THEN '45-54'
        ELSE '55+'
    END as age_group,
    COUNT(*) as total_count,
    SUM(CASE WHEN risk = 'Risk' THEN 1 ELSE 0 END) as high_risk_count,
    ROUND(100.0 * SUM(CASE WHEN risk = 'Risk' THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) as risk_percentage,
    ROUND(AVG(loan_amount), 2) as avg_loan_amount
FROM credit_applications
GROUP BY age_group
ORDER BY 
    CASE age_group
        WHEN 'Under 25' THEN 1
        WHEN '25-34' THEN 2
        WHEN '35-44' THEN 3
        WHEN '45-54' THEN 4
        ELSE 5
    END;

-- ============================================================================
-- QUERY 8: Top Risky Loan Combinations
-- COMMON MISTAKE: Missing validation of actual data values
-- ============================================================================

-- name: get_top_risky_combinations
-- ❌ BREAKING: Assuming risk values without checking actual data
-- ✅ FIXED: Test data validates 'Risk' is the correct value
SELECT 
    loan_purpose,
    employment_duration,
    COUNT(*) as occurrence_count,
    ROUND(AVG(loan_amount), 2) as avg_loan_amount,
    ROUND(AVG(age), 1) as avg_age
FROM credit_applications
WHERE risk = 'Risk'  -- Validated by test data
GROUP BY loan_purpose, employment_duration
HAVING COUNT(*) >= 3
ORDER BY occurrence_count DESC
LIMIT 10;

-- ============================================================================
-- REAL-WORLD EXAMPLE: What happens WITHOUT test data
-- ============================================================================

-- SCENARIO: Developer writes this query in isolation:
-- 
-- SELECT AVG(loan_amount) / COUNT(*)
-- FROM credit_applications
-- WHERE employment_duration = 'unemployed';
--
-- PROBLEMS:
-- 1. If no unemployed applicants exist → COUNT(*) = 0 → Division by zero error
-- 2. Developer doesn't know 'unemployed' isn't a valid value in the data
-- 3. Query returns NULL but developer expects a number
-- 4. Downstream application crashes when it tries to display the result
--
-- WITH OPTIM TEST DATA:
-- 1. Test runs query against 500 synthetic records
-- 2. Discovers 'unemployed' returns 0 rows (invalid value)
-- 3. Catches division by zero before commit
-- 4. Developer fixes query before it reaches production
-- 5. Commit is blocked until tests pass

-- Made with Bob