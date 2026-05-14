#!/usr/bin/env python3
"""
Unit Tests for Credit Risk Assessment Application
Tests run with synthetic data from Optim API BEFORE committing changes
"""

import unittest
import os
import sys
import csv
import json
import tempfile
from pathlib import Path
from urllib.parse import quote
from app import CreditRiskDatabase

# Add parent directories to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, grandparent_dir)
sys.path.insert(0, parent_dir)

from auth_helper import OptimAuthHelper

# Custom function to load config from root .env
def load_config_from_root_env():
    """Load configuration from root .env file"""
    config = {}
    # Navigate to root directory (two levels up from TDM/mock_app/)
    root_dir = Path(__file__).parent.parent.parent
    env_path = root_dir / '.env'
    
    if not env_path.exists():
        return config
    
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    
    return config


class TestCreditRiskApplication(unittest.TestCase):
    """Test suite for Credit Risk Application"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test database with synthetic data from Optim Database API"""
        print("\n" + "="*70)
        print("  PRE-COMMIT TESTING WITH OPTIM DATABASE API")
        print("  Fetching synthetic data directly from database")
        print("="*70 + "\n")
        
        cls.db = CreditRiskDatabase("test_credit_risk.db")
        cls.temp_csv = None
        
        # Load configuration from root .env
        config = load_config_from_root_env()
        
        if not all([config.get('OPTIM_BASE_URL'), config.get('OPTIM_USERNAME'), config.get('OPTIM_PASSWORD')]):
            raise RuntimeError(
                "Missing Optim configuration in .env file. "
                "Required: OPTIM_BASE_URL, OPTIM_USERNAME, OPTIM_PASSWORD"
            )
        
        try:
            # Authenticate with Optim API
            print("🔐 Authenticating with Optim API...")
            auth = OptimAuthHelper(
                config['OPTIM_BASE_URL'],
                config['OPTIM_USERNAME'],
                config['OPTIM_PASSWORD']
            )
            
            access_token = auth.get_access_token()
            if not access_token:
                raise RuntimeError("Authentication with Optim API failed")
            
            print("✅ Authentication successful\n")
            
            optim_client = cls._create_optim_client(
                config['OPTIM_BASE_URL'],
                access_token,
                config.get('OPTIM_ACCOUNT_ID'),
                config.get('OPTIM_CONN_PROFILE')
            )
            
            # Validate connection profile for Database API
            if not config.get('OPTIM_CONN_PROFILE'):
                raise RuntimeError(
                    "Missing OPTIM_CONN_PROFILE in .env file. "
                    "Database API requires 'optim-conn-profile' header."
                )
            
            print("📡 Fetching test data from Optim Database API...")
            
            # Fetch data directly from database using schema and table name
            schema_name = config.get('OPTIM_SCHEMA_NAME', 'OPTIM')
            table_name = config.get('OPTIM_TABLE_NAME', 'TDM - MODIFIED-BY-OPTIM')
            
            print(f"   Fetching from schema: {schema_name}, table: {table_name}")
            
            extracted_data = cls._fetch_rows_from_database(
                optim_client,
                schema_name,
                table_name,
                limit=500
            )
            
            if not extracted_data:
                raise RuntimeError(
                    f"No valid data retrieved from database table {schema_name}.{table_name}. "
                    "Expected actual rows with the required credit-risk columns."
                )
            
            print(f"✅ Retrieved {len(extracted_data)} records from database table\n")
            
            cls.temp_csv = cls._create_temp_csv(extracted_data)
            count = cls.db.load_test_data_from_csv(cls.temp_csv, limit=500)
            print(f"✅ Loaded {count} credit applications from Optim database for testing\n")
            
        except Exception as e:
            raise RuntimeError(f"Error fetching required Optim database data: {e}") from e
    
    @classmethod
    def _load_from_csv_fallback(cls):
        """Deprecated fallback retained for compatibility; tests now require Optim database data"""
        raise RuntimeError("Local CSV fallback is disabled; tests require actual Optim database data")
    
    @classmethod
    def _create_optim_client(cls, base_url, access_token, account_id=None, conn_profile=None):
        """Create Optim API client configuration"""
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        if account_id:
            headers['account-id'] = account_id
        if conn_profile:
            headers['optim-conn-profile'] = conn_profile
        
        return {
            'base_url': base_url.rstrip('/'),
            'headers': headers
        }
    
    @classmethod
    def _fetch_rows_from_database(cls, optim_client, schema_name, table_name, limit=500):
        """Fetch data directly from database using Database API"""
        import requests
        
        # Get table metadata first to understand column structure
        table_info = cls._get_database_table_info(optim_client, schema_name, table_name)
        if not table_info:
            return []
        
        columns = table_info.get('columns', [])
        if not columns:
            return []
        
        # Fetch actual data from the database table
        table_rows = cls._get_database_table_data(
            optim_client,
            schema_name,
            table_name,
            limit=limit
        )
        if not table_rows:
            return []
        
        # Normalize rows to dictionaries
        normalized_rows = cls._normalize_database_rows(
            columns,
            table_rows,
            schema_name,
            table_name
        )
        
        # Filter for credit risk rows
        credit_risk_rows = [row for row in normalized_rows if cls._is_credit_risk_row(row)]
        return credit_risk_rows
    
    @classmethod
    def _get_database_table_info(cls, optim_client, schema_name, table_name):
        """Get column metadata for a database table"""
        import requests
        
        # URL-encode the table name to handle special characters
        encoded_table = quote(table_name, safe='')
        url = f"{optim_client['base_url']}/v1/database/schemas/{schema_name}/tables/{encoded_table}"
        response = requests.get(url, headers=optim_client['headers'], verify=False)
        if response.status_code != 200:
            return {}
        
        result = response.json()
        
        # Handle different response formats - try multiple paths
        if isinstance(result, dict):
            # Try to extract columns from various possible locations
            columns = result.get('columns', [])
            
            # Try alternative paths for columns
            if not columns:
                request_obj = result.get('requestObj', {})
                if 'columns' in request_obj:
                    columns = request_obj['columns']
                elif 'table' in request_obj:
                    table_obj = request_obj.get('table', {})
                    if 'columns' in table_obj:
                        columns = table_obj['columns']
            
            # Return result with normalized columns
            if columns:
                result['columns'] = columns
        
        return result if isinstance(result, dict) else {}
    
    @classmethod
    def _get_database_table_data(cls, optim_client, schema_name, table_name, limit=500):
        """Get actual rows from a database table"""
        import requests
        
        # URL-encode the table name to handle special characters
        encoded_table = quote(table_name, safe='')
        url = f"{optim_client['base_url']}/v1/database/schemas/{schema_name}/tables/{encoded_table}/data"
        params = {'limit': limit}
        response = requests.get(url, headers=optim_client['headers'], params=params, verify=False)
        if response.status_code != 200:
            return []
        
        result = response.json()
        
        # Handle different response formats - try multiple paths for rows
        rows = []
        if isinstance(result, dict):
            rows = result.get('rows', [])
            
            # Try alternative paths for rows
            if not rows:
                request_obj = result.get('requestObj', {})
                if 'rows' in request_obj:
                    rows = request_obj['rows']
                elif 'resources' in request_obj:
                    rows = request_obj['resources']
        
        return rows
    
    @classmethod
    def _normalize_database_rows(cls, columns, raw_rows, schema_name, table_name):
        """Map database row arrays to dictionaries using column metadata"""
        normalized_rows = []
        column_names = [column.get('name') for column in columns]
        if not column_names or any(name is None for name in column_names):
            return []
        
        expected_field_map = {
            'CHECKINGSTATUS': 'CheckingStatus',
            'LOANDURATION': 'LoanDuration',
            'CREDITHISTORY': 'CreditHistory',
            'LOANPURPOSE': 'LoanPurpose',
            'LOANAMOUNT': 'LoanAmount',
            'EXISTINGSAVINGS': 'ExistingSavings',
            'EMPLOYMENTDURATION': 'EmploymentDuration',
            'INSTALLMENTPERCENT': 'InstallmentPercent',
            'SEX': 'Sex',
            'OTHERSONLOAN': 'OthersOnLoan',
            'CURRENTRESIDENCEDURATION': 'CurrentResidenceDuration',
            'OWNSPROPERTY': 'OwnsProperty',
            'AGE': 'Age',
            'INSTALLMENTPLANS': 'InstallmentPlans',
            'HOUSING': 'Housing',
            'EXISTINGCREDITSCOUNT': 'ExistingCreditsCount',
            'JOB': 'Job',
            'DEPENDENTS': 'Dependents',
            'TELEPHONE': 'Telephone',
            'FOREIGNWORKER': 'ForeignWorker',
            'RISK': 'Risk',
            'PREDICTED_LABEL': 'predicted_label',
            'PROBABILITY': 'probability'
        }
        
        for raw_row in raw_rows:
            if not isinstance(raw_row, list):
                continue
            row_dict = {}
            for index, column_name in enumerate(column_names):
                normalized_name = expected_field_map.get(column_name, column_name)
                row_dict[normalized_name] = raw_row[index] if index < len(raw_row) else None
            row_dict['_optim_schema'] = schema_name
            row_dict['_optim_table'] = table_name
            normalized_rows.append(row_dict)
        
        return normalized_rows
    
    @classmethod
    def _is_credit_risk_row(cls, row):
        """Check whether a row contains the fields needed by the mock app"""
        required_fields = [
            'CheckingStatus', 'LoanDuration', 'CreditHistory', 'LoanPurpose',
            'LoanAmount', 'ExistingSavings', 'EmploymentDuration', 'InstallmentPercent',
            'Sex', 'OthersOnLoan', 'CurrentResidenceDuration', 'OwnsProperty',
            'Age', 'InstallmentPlans', 'Housing', 'ExistingCreditsCount',
            'Job', 'Dependents', 'Telephone', 'ForeignWorker',
            'Risk', 'predicted_label', 'probability'
        ]
        return all(field in row and row[field] not in (None, '') for field in required_fields)
    
    @classmethod
    def _create_temp_csv(cls, extracted_data):
        """Create temporary CSV file from actual Optim database data"""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='')
        
        fieldnames = [
            'CheckingStatus', 'LoanDuration', 'CreditHistory', 'LoanPurpose',
            'LoanAmount', 'ExistingSavings', 'EmploymentDuration', 'InstallmentPercent',
            'Sex', 'OthersOnLoan', 'CurrentResidenceDuration', 'OwnsProperty',
            'Age', 'InstallmentPlans', 'Housing', 'ExistingCreditsCount',
            'Job', 'Dependents', 'Telephone', 'ForeignWorker',
            'Risk', 'predicted_label', 'probability'
        ]
        
        writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in extracted_data:
            if isinstance(row, dict):
                writer.writerow({field: row.get(field) for field in fieldnames})
        
        temp_file.close()
        return temp_file.name
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test database and temporary files"""
        cls.db.close()
        if os.path.exists("test_credit_risk.db"):
            os.remove("test_credit_risk.db")
        
        # Clean up temporary CSV file
        if cls.temp_csv and os.path.exists(cls.temp_csv):
            os.remove(cls.temp_csv)
    
    def test_01_database_setup(self):
        """Test database initialization"""
        stats = self.db.get_statistics()
        self.assertGreater(stats['total_applications'], 0, 
                          "Database should have applications")
        print("✅ Test 1: Database setup successful")
    
    def test_02_get_application_by_id(self):
        """Test retrieving application by ID"""
        app = self.db.get_application(1)
        self.assertIsNotNone(app, "Application with ID 1 should exist")
        assert app is not None
        self.assertIn('loan_amount', app, "Application should have loan_amount")
        self.assertIn('risk', app, "Application should have risk field")
        print(f"✅ Test 2: Get application by ID - Found ${app['loan_amount']} loan")
    
    def test_03_get_high_risk_applications(self):
        """Test retrieving high-risk applications"""
        high_risk = self.db.get_high_risk_applications()
        self.assertIsInstance(high_risk, list, "Should return a list")
        
        # Verify all returned applications are high risk
        for app in high_risk:
            self.assertEqual(app['risk'], 'Risk', 
                           "All applications should be marked as Risk")
        
        print(f"✅ Test 3: Get high-risk applications - Found {len(high_risk)} applications")
    
    def test_04_search_by_purpose(self):
        """Test searching applications by loan purpose"""
        purposes = ['furniture', 'car_new', 'education']
        
        for purpose in purposes:
            results = self.db.get_applications_by_purpose(purpose)
            self.assertIsInstance(results, list, "Should return a list")
            
            # Verify all results match the purpose
            for app in results:
                self.assertEqual(app['loan_purpose'], purpose,
                               f"All results should have purpose: {purpose}")
        
        print(f"✅ Test 4: Search by purpose - Tested {len(purposes)} purposes")
    
    def test_05_statistics_calculation(self):
        """Test database statistics"""
        stats = self.db.get_statistics()
        
        required_fields = ['total_applications', 'high_risk_count', 
                          'low_risk_count', 'risk_percentage',
                          'average_loan_amount', 'average_age']
        
        for field in required_fields:
            self.assertIn(field, stats, f"Stats should include {field}")
        
        # Verify calculations
        self.assertEqual(
            stats['total_applications'],
            stats['high_risk_count'] + stats['low_risk_count'],
            "Total should equal high risk + low risk"
        )
        
        self.assertGreater(stats['average_loan_amount'], 0,
                          "Average loan amount should be positive")
        self.assertGreater(stats['average_age'], 0,
                          "Average age should be positive")
        
        print(f"✅ Test 5: Statistics - {stats['total_applications']} total, "
              f"{stats['risk_percentage']:.1f}% high risk")
    
    def test_06_new_risk_assessment_logic(self):
        """
        Test NEW risk assessment logic (the feature we're testing!)
        This validates our code changes before committing
        """
        # Test case 1: Low risk scenario
        risk1 = self.db.assess_risk(
            loan_amount=3000,
            age=40,
            employment_duration='greater_7'
        )
        self.assertEqual(risk1, 'Low Risk',
                        "Small loan, mature age, stable employment should be low risk")
        
        # Test case 2: High risk scenario
        risk2 = self.db.assess_risk(
            loan_amount=15000,
            age=22,
            employment_duration='less_1'
        )
        self.assertEqual(risk2, 'High Risk',
                        "Large loan, young age, new employment should be high risk")
        
        # Test case 3: Medium risk scenario
        risk3 = self.db.assess_risk(
            loan_amount=7000,
            age=30,
            employment_duration='4_to_7'
        )
        self.assertEqual(risk3, 'Medium Risk',
                        "Medium loan, average age, moderate employment should be medium risk")
        
        # Test case 4: Edge case - employment duration impact
        risk4 = self.db.assess_risk(
            loan_amount=5000,
            age=35,
            employment_duration='less_1'
        )
        self.assertIn(risk4, ['Medium Risk', 'High Risk'],
                     "New employment should increase risk even with moderate loan")
        
        print("✅ Test 6: NEW risk assessment logic - All scenarios validated")
    
    def test_07_data_integrity(self):
        """Test data integrity and consistency"""
        stats = self.db.get_statistics()
        
        # Verify no negative values
        self.assertGreaterEqual(stats['total_applications'], 0,
                               "Total applications should not be negative")
        self.assertGreaterEqual(stats['high_risk_count'], 0,
                               "High risk count should not be negative")
        self.assertGreaterEqual(stats['average_loan_amount'], 0,
                               "Average loan amount should not be negative")
        
        # Verify risk percentage is valid
        self.assertGreaterEqual(stats['risk_percentage'], 0,
                               "Risk percentage should not be negative")
        self.assertLessEqual(stats['risk_percentage'], 100,
                            "Risk percentage should not exceed 100")
        
        print("✅ Test 7: Data integrity - All values within valid ranges")
    
    def test_08_synthetic_data_quality(self):
        """Verify synthetic data quality and privacy compliance"""
        # Get sample applications
        apps = []
        for i in range(1, 11):
            app = self.db.get_application(i)
            if app:
                apps.append(app)
        
        self.assertGreater(len(apps), 0, "Should have sample applications")
        
        # Verify data has realistic values
        for app in apps:
            self.assertGreater(app['loan_amount'], 0,
                             "Loan amount should be positive")
            self.assertGreater(app['age'], 18,
                             "Age should be adult")
            self.assertLess(app['age'], 100,
                           "Age should be realistic")
            self.assertIn(app['risk'], ['Risk', 'No Risk'],
                         "Risk should be valid value")
        
        print(f"✅ Test 8: Synthetic data quality - Validated {len(apps)} records")


def run_tests():
    """Run all tests and generate report"""
    print("🚀 Starting pre-commit test suite...")
    print("   Testing code changes with synthetic data from Optim\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCreditRiskApplication)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("  TEST SUMMARY")
    print("="*70)
    print(f"Tests Run: {result.testsRun}")
    print(f"✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failed: {len(result.failures)}")
    print(f"⚠️  Errors: {len(result.errors)}")
    print("="*70 + "\n")
    
    if result.wasSuccessful():
        print("🎉 ALL TESTS PASSED!")
        print("✅ Your code changes are validated with synthetic test data")
        print("✅ Safe to commit and push your changes")
        print("\nNext steps:")
        print("  git add .")
        print("  git commit -m 'Enhanced risk assessment logic'")
        print("  git push")
        return 0
    else:
        print("❌ TESTS FAILED!")
        print("⚠️  DO NOT COMMIT - Fix the issues first")
        print("\nFailed tests indicate:")
        print("  • Your code changes may have introduced bugs")
        print("  • Logic errors in the new risk assessment")
        print("  • Data handling issues")
        print("\nFix the issues and run tests again:")
        print("  python3 test_app.py")
        return 1


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)

# Made with Bob
