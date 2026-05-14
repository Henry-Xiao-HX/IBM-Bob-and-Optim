# IBM Optim Test Data Management (TDM)

**Synthetic Test Data Generation for DevOps CI/CD Teams**

Generate privacy-compliant, production-like test data directly in your IDE using IBM Optim Archive APIs.

---

## 🎯 Overview

This toolkit enables DevOps teams to:

- **🔍 Discover** production data structures without accessing sensitive data
- **✂️ Subset** production data for manageable test environments
- **🔒 Mask** sensitive information for privacy compliance (GDPR, HIPAA, etc.)
- **🎲 Generate** synthetic test data with production-like patterns
- **🚀 Integrate** seamlessly into CI/CD pipelines

## ✨ Key Benefits for DevOps Teams

| Benefit | Description |
|---------|-------------|
| **Privacy Compliant** | Automatic masking of PII, PHI, and sensitive data |
| **Production-Like** | Maintains data patterns and referential integrity |
| **Automated** | No manual test data creation needed |
| **CI/CD Ready** | Export to JSON, SQL, CSV for pipeline integration |
| **Scalable** | Generate any volume of test data on-demand |
| **IDE-Native** | Work directly in VS Code with IBM BOB |

---

## 🚀 Quick Start

### Prerequisites

1. **IBM Optim Archive** configured with archived production data
2. **Python 3.7+** installed
3. **API credentials** (username, password, base URL)

### Setup

```bash
# 1. Navigate to TDM directory
cd TDM

# 2. Configure credentials (use parent .env file)
# Ensure your .env file contains:
# OPTIM_BASE_URL=https://your-optim-server:7725/optim
# OPTIM_USERNAME=your_username
# OPTIM_PASSWORD=your_password

# 3. Run the demo
python3 synthetic_testdata_demo.py
```

### What Happens

The demo will:
1. ✅ Authenticate with Optim API
2. ✅ Discover available production data sources
3. ✅ Analyze table structures and metadata
4. ✅ Subset production data (configurable size)
5. ✅ Apply privacy masking to sensitive fields
6. ✅ Generate synthetic test data
7. ✅ Export in multiple formats (JSON, SQL, CSV)
8. ✅ Create CI/CD integration scripts

---

## 📊 Demo Walkthrough

### Step 1: Data Discovery

```python
# Discovers all available archive jobs
jobs = generator.discover_data_sources()

# Output:
# ✅ Found 3 data source(s) available for testing
# 
# 📦 Data Source 1:
#    • Name: Customer Archive 2024
#    • ID: job-123
#    • Source: PROD_DB
#    • Status: FINISHED
```

### Step 2: Schema Discovery

```python
# Discovers schemas and tables
schema_map = generator.discover_schemas_and_tables(job_id)

# Output:
# ✅ Found 2 schema(s)
# 
# 📁 Schema: public
#    Tables (5): customers, orders, products, payments, reviews
```

### Step 3: Table Analysis

```python
# Analyzes table structure
table_info = generator.analyze_table_structure(job_id, schema, table)

# Output:
# ✅ Table Metadata Retrieved
# 
# 📋 Table: public.customers
#    • Total Rows: 50,000
#    • Columns: 12
# 
# 🔑 Column Structure:
#    • customer_id        INTEGER         NOT NULL [PK]
#    • email              VARCHAR         NULL
#    • phone              VARCHAR         NULL
#    • first_name         VARCHAR         NOT NULL
#    • last_name          VARCHAR         NOT NULL
```

### Step 4: Data Subsetting

```python
# Extracts a subset of production data
subset_rows = generator.subset_production_data(job_id, schema, table, limit=100)

# Output:
# ✅ Extracted 100 rows for testing
# 
# 💾 Data Subset Summary:
#    • Source: public.customers
#    • Rows Retrieved: 100
#    • Columns: 12
#    • Subset Ratio: 0.20% of production
```

### Step 5: Data Masking

```python
# Applies privacy masking
masked_rows = generator.apply_data_masking(subset_rows, ['email', 'phone', 'ssn'])

# Output:
# 🛡️  Masking Strategy:
#    • email: email masking
#    • phone: phone masking
#    • ssn: ssn masking
# 
# ✅ Masked 100 rows
#    • Sensitive columns protected: 3
#    • Data patterns preserved: Yes
#    • Referential integrity: Maintained
```

**Before Masking:**
```json
{
  "customer_id": 1001,
  "email": "john.doe@realcompany.com",
  "phone": "415-555-1234",
  "ssn": "123-45-6789"
}
```

**After Masking:**
```json
{
  "customer_id": 1001,
  "email": "user7234@testdata.com",
  "phone": "555-892-4561",
  "ssn": "XXX-XX-4892"
}
```

### Step 6: Synthetic Data Generation

```python
# Generates synthetic test data
synthetic_rows = generator.generate_synthetic_data(table_info, num_rows=50)

# Output:
# 🔧 Generation Strategy:
#    • customer_id: Sequential ID
#    • email: Synthetic email
#    • phone: Random phone
#    • created_at: Random date range
#    • status: Type-appropriate value
# 
# ✅ Generated 50 synthetic records
#    • Data quality: Production-like
#    • Referential integrity: Maintained
#    • Privacy compliant: Yes
```

### Step 7: Export for CI/CD

```python
# Exports in multiple formats
json_file = generator.export_test_data(synthetic_rows, format='json')
sql_file = generator.export_test_data(synthetic_rows, format='sql')
csv_file = generator.export_test_data(synthetic_rows, format='csv')

# Output:
# ✅ Test data exported successfully
#    • File: synthetic_test_data.json
#    • Format: JSON
#    • Records: 50
#    • Size: 12.45 KB
```

---

## 🔒 Data Masking Capabilities

### Supported Masking Types

| Data Type | Masking Strategy | Example |
|-----------|------------------|---------|
| **Email** | Synthetic email addresses | `user1234@testdata.com` |
| **Phone** | Random phone numbers | `555-892-4561` |
| **SSN** | Partial masking | `XXX-XX-4892` |
| **Credit Card** | Partial masking | `XXXX-XXXX-XXXX-4892` |
| **Names** | Random name generation | `John Smith` |
| **Addresses** | Synthetic addresses | `1234 Test St, TestCity, TS 12345` |
| **Generic** | Type-appropriate masking | `MASKED_7234` |

### Auto-Detection

The system automatically detects sensitive columns based on naming patterns:

```python
# Automatically masked columns:
- email, email_address, user_email
- phone, phone_number, telephone, mobile
- ssn, social_security, social_security_number
- credit_card, card_number, cc_number
- first_name, last_name, full_name, customer_name
- address, street_address, billing_address
```

---

## 🚀 CI/CD Integration

### Generated Artifacts

After running the demo, you'll have:

1. **`synthetic_test_data.json`** - JSON format for API testing
2. **`synthetic_test_data.sql`** - SQL INSERT statements
3. **`synthetic_test_data.csv`** - CSV format for data tools
4. **`load_test_data.sh`** - CI/CD integration script

### Integration Examples

#### Jenkins Pipeline

```groovy
pipeline {
    agent any
    stages {
        stage('Generate Test Data') {
            steps {
                sh 'python3 TDM/synthetic_testdata_demo.py'
            }
        }
        stage('Load Test Data') {
            steps {
                sh './load_test_data.sh'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'npm test'
            }
        }
    }
}
```

#### GitHub Actions

```yaml
name: Test with Synthetic Data

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Generate Test Data
        run: python3 TDM/synthetic_testdata_demo.py
        env:
          OPTIM_BASE_URL: ${{ secrets.OPTIM_BASE_URL }}
          OPTIM_USERNAME: ${{ secrets.OPTIM_USERNAME }}
          OPTIM_PASSWORD: ${{ secrets.OPTIM_PASSWORD }}
      
      - name: Load Test Data
        run: ./load_test_data.sh
      
      - name: Run Tests
        run: npm test
```

#### GitLab CI

```yaml
test:
  stage: test
  script:
    - python3 TDM/synthetic_testdata_demo.py
    - ./load_test_data.sh
    - npm test
  variables:
    OPTIM_BASE_URL: $OPTIM_BASE_URL
    OPTIM_USERNAME: $OPTIM_USERNAME
    OPTIM_PASSWORD: $OPTIM_PASSWORD
```

---

## 🛠️ Advanced Usage

### Programmatic Usage

```python
from synthetic_testdata_demo import SyntheticTestDataGenerator
from auth_helper import OptimAuthHelper, load_config_from_env

# Setup
config = load_config_from_env()
auth = OptimAuthHelper(
    config['OPTIM_BASE_URL'],
    config['OPTIM_USERNAME'],
    config['OPTIM_PASSWORD']
)
token = auth.get_access_token()

# Create generator
generator = SyntheticTestDataGenerator(
    base_url=config['OPTIM_BASE_URL'],
    access_token=token
)

# Generate test data
jobs = generator.discover_data_sources()
job_id = jobs[0]['id']

schema_map = generator.discover_schemas_and_tables(job_id)
schema = list(schema_map.keys())[0]
table = schema_map[schema][0]

table_info = generator.analyze_table_structure(job_id, schema, table)
synthetic_data = generator.generate_synthetic_data(table_info, num_rows=100)

# Export
generator.export_test_data(synthetic_data, format='json', filename='my_test_data')
```

### Custom Masking Rules

```python
# Add custom masking function
def mask_employee_id(value):
    return f"EMP{random.randint(10000, 99999)}"

# Apply custom masking
generator._mask_employee_id = mask_employee_id
```

### Batch Generation

```python
# Generate multiple tables
for schema, tables in schema_map.items():
    for table in tables:
        table_info = generator.analyze_table_structure(job_id, schema, table)
        synthetic_data = generator.generate_synthetic_data(table_info, num_rows=100)
        generator.export_test_data(
            synthetic_data, 
            format='sql', 
            filename=f'{schema}_{table}_test_data'
        )
```

---

## 📋 Use Cases

### 1. **Development Environment Setup**

Generate test data for local development:

```bash
python3 synthetic_testdata_demo.py
# Creates: synthetic_test_data.sql
psql -d dev_db -f synthetic_test_data.sql
```

### 2. **Automated Testing**

Integrate into test suites:

```python
# test_setup.py
def setup_test_data():
    generator = SyntheticTestDataGenerator(...)
    test_data = generator.generate_synthetic_data(table_info, num_rows=50)
    load_into_test_db(test_data)
```

### 3. **Performance Testing**

Generate large datasets:

```python
# Generate 10,000 records for load testing
large_dataset = generator.generate_synthetic_data(table_info, num_rows=10000)
generator.export_test_data(large_dataset, format='sql', filename='load_test_data')
```

### 4. **Demo Environments**

Create realistic demo data:

```python
# Generate demo data with specific patterns
demo_data = generator.generate_synthetic_data(table_info, num_rows=200)
generator.export_test_data(demo_data, format='json', filename='demo_data')
```

---

## 🔐 Security & Compliance

### Privacy Features

- ✅ **No Production Data Exposure** - Only metadata is accessed
- ✅ **Automatic PII Masking** - Sensitive fields automatically detected
- ✅ **Configurable Masking** - Custom rules for your data
- ✅ **Audit Trail** - All operations logged
- ✅ **Token-Based Auth** - Secure API access

### Compliance Standards

| Standard | Support |
|----------|---------|
| **GDPR** | ✅ PII masking and data minimization |
| **HIPAA** | ✅ PHI masking and access controls |
| **PCI DSS** | ✅ Credit card masking |
| **SOC 2** | ✅ Audit logging and access controls |

---

## 🎓 Best Practices

### 1. **Start Small**

Begin with a small subset (50-100 rows) to validate:
- Data structure
- Masking rules
- Export format

### 2. **Validate Referential Integrity**

Ensure foreign keys are maintained:
```python
# Check relationships before generation
validate_foreign_keys(table_info)
```

### 3. **Version Control Test Data**

Store generated SQL in version control:
```bash
git add test_data/*.sql
git commit -m "Update test data for v2.0"
```

### 4. **Automate Refresh**

Schedule regular test data updates:
```bash
# Cron job: Daily at 2 AM
0 2 * * * cd /path/to/TDM && python3 synthetic_testdata_demo.py
```

### 5. **Document Masking Rules**

Maintain documentation of what's masked:
```markdown
# Masking Rules
- customer_email: Synthetic emails
- customer_phone: Random 555 numbers
- ssn: XXX-XX-#### format
```

---

## 🐛 Troubleshooting

### Authentication Issues

```bash
# Verify credentials
python3 -c "from auth_helper import *; print(load_config_from_env())"

# Test connection
curl -k -X POST https://your-server:7725/optim/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"pass"}'
```

### No Data Sources Found

1. Verify Optim Archive has completed jobs
2. Check user permissions
3. Confirm API endpoint is correct

### Export Errors

```python
# Check write permissions
import os
print(os.access('.', os.W_OK))  # Should be True

# Verify disk space
import shutil
print(shutil.disk_usage('.'))
```

---

## 📞 Support

For issues or questions:

1. **Check Documentation** - Review this README and API docs
2. **Review Examples** - See `../examples/` directory
3. **Check Logs** - Review console output for errors
4. **Contact Support** - Reach out to your IBM Optim administrator

---

## 🎯 Next Steps

1. **Run the Demo** - `python3 synthetic_testdata_demo.py`
2. **Customize Masking** - Add your own masking rules
3. **Integrate CI/CD** - Add to your pipeline
4. **Scale Up** - Generate larger datasets
5. **Automate** - Schedule regular data refresh

---

## 📚 Additional Resources

- [IBM Optim Archive API Documentation](../docs/API_REFERENCE.md)
- [Parent Project README](../README.md)
- [Authentication Guide](../examples/basic_authentication.py)
- [Dashboard Monitoring](../dashboard/README.md)

---

**Built for DevOps teams who need production-like test data without the privacy risks** 🎯