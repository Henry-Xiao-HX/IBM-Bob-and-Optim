# IBM Optim Test Data Management (TDM)

**Synthetic Test Data Generation for DevOps CI/CD Teams**

Generate privacy-compliant, production-like test data directly in your IDE using IBM Optim Archive APIs.

---

## Overview

This [`TDM`](README.md) area provides:
- a high-level IBM Optim TDM workflow for synthetic test data
- guidance for masking and privacy-safe development
- CI/CD integration patterns
- a runnable mock application under [`TDM/mock_app`](mock_app/README.md)

## Key benefits

| Benefit | Description |
|---------|-------------|
| Privacy compliant | Automatic masking of PII, PHI, and sensitive data |
| Production-like | Maintains data patterns and referential integrity |
| Automated | Reduces manual test data creation |
| CI/CD ready | Export to JSON, SQL, CSV for pipeline integration |
| Scalable | Generate any volume of test data on demand |
| IDE-native | Works directly in VS Code with IBM BOB |

---

## Structure

- **[`TDM/mock_app`](mock_app/README.md)** - Credit risk mock app, SQL validation flow, and local pre-commit workflow
- **[`docs/optim-tdm-1.1.0_api-docs.yaml`](../docs/optim-tdm-1.1.0_api-docs.yaml)** - Optim TDM API contract
- **[`auth_helper.py`](../auth_helper.py)** - Shared authentication helper used across examples and demos

Use this README for the shared TDM concepts. Use [`TDM/mock_app/README.md`](mock_app/README.md) for the app-specific workflow.

---

## Quick start

### Prerequisites

1. IBM Optim Archive configured with archived production data
2. Python 3.7+
3. API credentials in the repository-level environment file

### Setup

Create a repository-level [`.env`](../.env.example) based on [`.env.example`](../.env.example) and set:

```bash
OPTIM_BASE_URL=https://your-optim-server:7725/optim
OPTIM_USERNAME=your_username
OPTIM_PASSWORD=your_password
OPTIM_ACCOUNT_ID=your_account_id
```

Then run the mock workflow from [`TDM/mock_app`](mock_app/README.md):

```bash
cd TDM/mock_app
pip install -r ../../requirements.txt
./run_tests.sh
```

Optional: install the local pre-commit hook:

```bash
./setup_git_hook.sh
```

---

## Shared TDM workflow

IBM Optim TDM generally follows this pattern:

1. **Discover** archive jobs and data sources
2. **Inspect** schemas, tables, and metadata
3. **Subset** source data into manageable testing volumes
4. **Mask** sensitive values for privacy compliance
5. **Generate** production-like synthetic records
6. **Export** test data for local or pipeline execution
7. **Validate** application logic and SQL before commit or deployment

This repository’s mock workflow demonstrates that pattern in a narrow, practical scenario using the credit-risk example in [`TDM/mock_app`](mock_app/README.md).

---

## Data masking capabilities

### Supported masking patterns

| Data type | Example masking result |
|-----------|------------------------|
| Email | `user1234@testdata.com` |
| Phone | `555-892-4561` |
| SSN | `XXX-XX-4892` |
| Credit card | `XXXX-XXXX-XXXX-4892` |
| Names | Synthetic first/last names |
| Addresses | Synthetic address values |
| Generic strings | Type-appropriate masked placeholders |

### Common auto-detected sensitive fields

Typical naming patterns include:
- `email`, `email_address`, `user_email`
- `phone`, `phone_number`, `telephone`, `mobile`
- `ssn`, `social_security`, `social_security_number`
- `credit_card`, `card_number`, `cc_number`
- `first_name`, `last_name`, `full_name`, `customer_name`
- `address`, `street_address`, `billing_address`

### Compliance alignment

| Standard | Typical support |
|----------|-----------------|
| GDPR | PII masking and data minimization |
| HIPAA | PHI masking and controlled access |
| PCI DSS | Card-number masking |
| SOC 2 | Auditability and access control support |

---

## CI/CD integration patterns

Generated or fetched synthetic data can be used in:
- local pre-commit validation
- pull request checks
- integration tests
- performance and demo environments

### Example: GitHub Actions

```yaml
name: Test with Synthetic Data

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

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

      - name: Run mock app tests
        run: cd TDM/mock_app && ./run_tests.sh

      - name: Run SQL validation
        run: cd TDM/mock_app && python3 test_sql.py
```

---

## Best practices

1. **Start small**  
   Validate with small datasets first before scaling volumes.

2. **Keep privacy first**  
   Never use raw production data in local or CI test environments.

3. **Automate validation**  
   Run application and SQL tests automatically before merge or deploy.

4. **Preserve fallback paths**  
   Keep local fallback datasets such as [`credit_risk_mock_data.csv`](mock_app/credit_risk_mock_data.csv) for offline development.

5. **Document app-specific workflows locally**  
   Keep shared TDM guidance here, and place scenario-specific instructions in local READMEs like [`TDM/mock_app/README.md`](mock_app/README.md).

---

## Troubleshooting

### Missing configuration

Ensure the repository-level [`.env`](../.env.example) exists and contains valid credentials.

### Authentication problems

Verify:
- `OPTIM_BASE_URL`
- `OPTIM_USERNAME`
- `OPTIM_PASSWORD`

### No data sources or archive jobs

Check that:
- Optim Archive is configured correctly
- archive jobs have completed
- the configured account has permission to access the data

### Offline or fallback mode

When Optim is unavailable, local workflows may fall back to static synthetic datasets such as [`credit_risk_mock_data.csv`](mock_app/credit_risk_mock_data.csv).

---

## Where to go next

- Run the mock workflow in [`TDM/mock_app`](mock_app/README.md)
- Review the root [`README.md`](../README.md) for broader repository context
- Inspect [`docs/optim-tdm-1.1.0_api-docs.yaml`](../docs/optim-tdm-1.1.0_api-docs.yaml) for API details

---

**Built for teams who need production-like test data without privacy risk**