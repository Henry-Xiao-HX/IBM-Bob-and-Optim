# Credit Risk Assessment Application - TDM Demo

This demo showcases IBM Optim Archive's Test Data Management (TDM) workflow for pre-commit testing with synthetic data.

## Overview

The application demonstrates how to:
1. **Fetch synthetic test data** directly from Optim Archive API
2. **Run pre-commit tests** with fresh, privacy-compliant data
3. **Validate code changes** before deployment
4. **Ensure data quality** without exposing sensitive information

## Files

- **`app.py`** - Credit risk assessment application with NEW risk assessment logic
- **`test_app.py`** - Unit tests that fetch synthetic data from Optim API
- **`credit_risk_mock_data.csv`** - Fallback CSV file (used when Optim API is unavailable)

## Setup

### 1. Configure Optim API Credentials

Create a `.env` file in the project root with your Optim credentials:

```bash
OPTIM_BASE_URL=https://your-optim-server:7725/optim
OPTIM_USERNAME=your_username
OPTIM_PASSWORD=your_password
OPTIM_ACCOUNT_ID=your_account_id  # Optional
```

### 2. Install Dependencies

```bash
pip install -r ../../requirements.txt
```

## Usage

### Run the Application Demo

```bash
python3 app.py
```

This demonstrates the credit risk assessment application with sample data.

### Run Pre-Commit Tests with Optim API

**Option 1: Using the helper script (recommended)**
```bash
./run_tests.sh
```

**Option 2: Run tests directly**
```bash
python3 test_app.py
```

**What happens:**
1. ✅ Authenticates with Optim Archive API
2. ✅ Fetches synthetic test data in real-time
3. ✅ Generates 500 synthetic credit applications
4. ✅ Loads data into test database
5. ✅ Runs 8 comprehensive unit tests
6. ✅ Validates NEW risk assessment logic
7. ✅ Reports test results

**If Optim API is unavailable:**
- Automatically falls back to local CSV file
- Tests still run successfully
- Warning message displayed

## Automated Pre-Commit Testing Workflow

### Git Hook Integration

This project includes an **automated pre-commit hook** that runs tests whenever you commit changes to [`app.py`](app.py:1).

#### How It Works

1. **Automatic Detection**: When you commit changes to [`app.py`](app.py:1), the Git hook automatically triggers
2. **Test Execution**: Runs [`test_app.py`](test_app.py:1) with synthetic data from Optim API
3. **Validation**: All 8 tests must pass before the commit is allowed
4. **Feedback**: Provides clear success/failure messages with colored output

#### Setup (Already Configured)

The pre-commit hook is already set up in this repository:
- **Hook Script**: [`.git/hooks/pre_commit_test_app_tdm`](../../.git/hooks/pre_commit_test_app_tdm:1)
- **Active Link**: [`.git/hooks/pre-commit`](../../.git/hooks/pre-commit:1) → `pre_commit_test_app_tdm`
- **Helper Script**: [`run_tests.sh`](run_tests.sh:1) for manual testing

#### Workflow Example

```bash
# 1. Make changes to app.py
vim app.py

# 2. Stage your changes
git add app.py

# 3. Commit (tests run automatically)
git commit -m "Enhanced risk assessment logic"

# Output:
═══════════════════════════════════════════════════════════════════
  PRE-COMMIT REVIEW: TDM/mock_app/app.py MODIFIED
═══════════════════════════════════════════════════════════════════

🔍 Detected changes to TDM/mock_app/app.py
🧪 Running automated test suite with synthetic data...

[Tests run automatically...]

✅ ALL TESTS PASSED - COMMIT APPROVED
Your changes to app.py have been validated with synthetic test data.
Proceeding with commit...

[main abc1234] Enhanced risk assessment logic
 1 file changed, 15 insertions(+), 5 deletions(-)
```

#### If Tests Fail

```bash
❌ TESTS FAILED - COMMIT BLOCKED

Your changes to app.py failed the test suite.
Please fix the issues before committing.

To fix:
  1. Review the test failures above
  2. Fix the issues in TDM/mock_app/app.py
  3. Run tests manually: cd TDM/mock_app && python3 test_app.py
  4. Try committing again once tests pass

To bypass this check (NOT RECOMMENDED):
  git commit --no-verify
```

#### Manual Testing Before Commit

Test your changes before committing:

```bash
# Run tests manually
./run_tests.sh

# Or directly
python3 test_app.py
```

#### Bypassing the Hook (Emergency Only)

```bash
# Skip pre-commit tests (NOT RECOMMENDED)
git commit --no-verify -m "Emergency fix"
```

⚠️ **Warning**: Bypassing tests can introduce bugs into the codebase.

#### Hook Management

**Disable the hook temporarily:**
```bash
rm .git/hooks/pre-commit
```

**Re-enable the hook:**
```bash
cd .git/hooks
ln -sf pre_commit_test_app_tdm pre-commit
```

**Modify the hook:**
```bash
vim .git/hooks/pre_commit_test_app_tdm
# Changes take effect immediately
```

## TDM Workflow

### Traditional Approach (Manual)
```
Developer → Manually create test data → Run tests → Commit
```
**Problems:**
- Time-consuming manual data creation
- Risk of using production data
- Privacy compliance issues
- Stale test data

### Optim TDM Approach (Automated)
```
Developer → test_app.py → Optim API → Synthetic data → Run tests → Commit
```
**Benefits:**
- ✅ Automated synthetic data generation
- ✅ Privacy-compliant test data
- ✅ Fresh data for every test run
- ✅ Production-like data patterns
- ✅ No manual data creation needed

## Test Coverage

The test suite validates:

1. **Database Setup** - Verifies database initialization
2. **Data Retrieval** - Tests application by ID lookup
3. **Risk Filtering** - Validates high-risk application queries
4. **Search Functionality** - Tests loan purpose searches
5. **Statistics** - Verifies aggregate calculations
6. **NEW Risk Assessment** - Tests enhanced risk logic with employment duration
7. **Data Integrity** - Ensures valid data ranges
8. **Data Quality** - Validates synthetic data realism

## Example Output

```
======================================================================
  PRE-COMMIT TESTING WITH OPTIM API
  Fetching synthetic data in real-time
======================================================================

🔐 Authenticating with Optim API...
✅ Using cached access token
✅ Authentication successful

📡 Fetching synthetic test data from Optim Archive...
   Using job: Credit_Risk_Archive
   Using table: CREDIT_SCHEMA.APPLICATIONS
🎲 Generating synthetic test data...
✅ Generated 500 synthetic records

✅ Loaded 500 synthetic credit applications for testing

✅ Test 1: Database setup successful
✅ Test 2: Get application by ID - Found $5804 loan
✅ Test 3: Get high-risk applications - Found 163 applications
✅ Test 4: Search by purpose - Tested 3 purposes
✅ Test 5: Statistics - 500 total, 32.6% high risk
✅ Test 6: NEW risk assessment logic - All scenarios validated
✅ Test 7: Data integrity - All values within valid ranges
✅ Test 8: Synthetic data quality - Validated 10 records

======================================================================
  TEST SUMMARY
======================================================================
Tests Run: 8
✅ Passed: 8
❌ Failed: 0
⚠️  Errors: 0
======================================================================

🎉 ALL TESTS PASSED!
✅ Your code changes are validated with synthetic test data
✅ Safe to commit and push your changes

Next steps:
  git add .
  git commit -m 'Enhanced risk assessment logic'  # Tests run automatically!
  git push
```

**Note**: With the pre-commit hook enabled, tests run automatically during `git commit`.

## CI/CD Integration

Integrate into your CI/CD pipeline:

```yaml
# .github/workflows/test.yml
name: Pre-Commit Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Configure Optim API
        env:
          OPTIM_BASE_URL: ${{ secrets.OPTIM_BASE_URL }}
          OPTIM_USERNAME: ${{ secrets.OPTIM_USERNAME }}
          OPTIM_PASSWORD: ${{ secrets.OPTIM_PASSWORD }}
        run: |
          echo "OPTIM_BASE_URL=$OPTIM_BASE_URL" > .env
          echo "OPTIM_USERNAME=$OPTIM_USERNAME" >> .env
          echo "OPTIM_PASSWORD=$OPTIM_PASSWORD" >> .env
      
      - name: Run tests with Optim synthetic data
        run: cd TDM/mock_app && ./run_tests.sh
```

**Note**: The pre-commit hook provides local validation, while CI/CD provides additional validation on the server.

## Benefits for DevOps Teams

### 1. **Automated Test Data Generation**
- No manual data creation required
- Fresh data for every test run
- Consistent data quality

### 2. **Privacy Compliance**
- No production data exposure
- Synthetic data mimics production patterns
- GDPR/CCPA compliant

### 3. **CI/CD Ready**
- API-driven workflow
- Easy pipeline integration
- Automated validation

### 4. **Developer Productivity**
- Focus on code, not test data
- Fast feedback loop
- Confident deployments

## Troubleshooting

### "Missing Optim configuration" Error

**Solution:** Create `.env` file with Optim credentials (see Setup section)

### "Authentication failed" Error

**Solution:** Verify credentials in `.env` file are correct

### "No archive jobs found" Error

**Solution:** Ensure Optim Archive has at least one configured archive job

### Tests Fall Back to CSV

**Expected behavior** when:
- `.env` file is missing
- Optim API is unavailable
- Network connectivity issues

Tests will still run successfully using the local CSV file.

## Best Practices

### Pre-Commit Testing
1. **Run tests before committing**: Use `./run_tests.sh` to catch issues early
2. **Don't bypass the hook**: Only use `--no-verify` in emergencies
3. **Keep tests fast**: Limit synthetic data to 500 records for quick feedback
4. **Update tests with code**: When adding features, add corresponding tests

### Test Data Management
1. **Use Optim API**: Prefer real-time synthetic data over static CSV
2. **Keep CSV updated**: Maintain fallback data for offline development
3. **Validate data quality**: Ensure synthetic data matches production patterns
4. **Privacy first**: Never use production data in tests

## Next Steps

1. **Customize Data Generation** - Modify `_create_temp_csv()` in [`test_app.py`](test_app.py:178) to match your data schema
2. **Add More Tests** - Extend test suite for additional features
3. **Integrate with CI/CD** - Add to your deployment pipeline (see CI/CD Integration section)
4. **Scale to Multiple Environments** - Use different Optim jobs for dev/staging/prod
5. **Share with Team** - Ensure all developers have the pre-commit hook enabled

## Support

For questions or issues:
- Review the main [README](../../README.md)
- Check [API Documentation](../../docs/API_REFERENCE.md)
- Contact your Optim administrator

---

**Made with Bob** 🤖