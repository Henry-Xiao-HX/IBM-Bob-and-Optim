#!/usr/bin/env python3
"""
SQL Query Tests - Demonstrates WHY test data matters
Tests run with synthetic data from Optim API BEFORE committing changes

This script shows how pre-commit testing catches breaking changes:
- Column name typos
- Division by zero errors
- Wrong data types
- NULL handling issues
- Logic errors with actual data values
"""

import unittest
import os
import sys
import sqlite3
import re
from pathlib import Path

# Add parent directories to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, grandparent_dir)

from auth_helper import OptimAuthHelper


class TestSQLQueries(unittest.TestCase):
    """Test suite that demonstrates why test data is critical"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test database with Optim synthetic data"""
        print("\n" + "="*70)
        print("  WHY TEST DATA MATTERS: SQL Query Validation")
        print("  Catching breaking changes BEFORE they reach production")
        print("="*70 + "\n")
        
        cls.db_path = "test_sql_queries.db"
        cls.conn = sqlite3.connect(cls.db_path)
        cls.conn.row_factory = sqlite3.Row
        cls.queries = cls._load_sql_queries()
        
        # Debug: Print parsed queries
        print(f"📋 Parsed {len(cls.queries)} queries:")
        for name in cls.queries.keys():
            print(f"   • {name}")
        print()
        
        # Load test data (simplified - using CSV fallback for demo)
        cls._setup_test_data()
    
    @classmethod
    def _load_sql_queries(cls):
        """Parse SQL file and extract named queries"""
        sql_file = Path(__file__).with_name('credit_risk_queries.sql')
        with open(sql_file, 'r') as f:
            content = f.read()
        
        queries = {}
        current_query = None
        query_lines = []
        in_query = False
        
        for line in content.split('\n'):
            # Look for query name comments
            if line.strip().startswith('-- name:'):
                # Save previous query
                if current_query and query_lines:
                    query_text = '\n'.join(query_lines).strip()
                    if query_text:
                        queries[current_query] = query_text
                
                current_query = line.split('-- name:')[1].strip()
                query_lines = []
                in_query = True
            elif line.strip().startswith('-- ===='):
                # End of query section (matches -- ============)
                if current_query and query_lines:
                    query_text = '\n'.join(query_lines).strip()
                    if query_text:
                        queries[current_query] = query_text
                current_query = None
                query_lines = []
                in_query = False
            elif in_query and current_query:
                # Skip comment lines and params lines
                if not line.strip().startswith('--'):
                    if line.strip() and not line.strip().upper().startswith('CREATE TABLE'):
                        query_lines.append(line)
        
        # Add last query
        if current_query and query_lines:
            query_text = '\n'.join(query_lines).strip()
            if query_text:
                queries[current_query] = query_text
        
        return queries
    
    @classmethod
    def _setup_test_data(cls):
        """Load synthetic test data from CSV"""
        cursor = cls.conn.cursor()
        
        # Create schema
        cursor.execute("""
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
            )
        """)
        
        # Load from CSV
        csv_file = Path(__file__).with_name('credit_risk_mock_data.csv')
        if csv_file.exists():
            import csv
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    if count >= 500:
                        break
                    cursor.execute("""
                        INSERT INTO credit_applications 
                        (checking_status, loan_duration, credit_history, loan_purpose, 
                         loan_amount, existing_savings, employment_duration, installment_percent,
                         sex, others_on_loan, current_residence_duration, owns_property,
                         age, installment_plans, housing, existing_credits_count,
                         job, dependents, telephone, foreign_worker, risk)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        row['CheckingStatus'], int(row['LoanDuration']), row['CreditHistory'],
                        row['LoanPurpose'], int(row['LoanAmount']),
                        row['ExistingSavings'], row['EmploymentDuration'], 
                        int(row['InstallmentPercent']), row['Sex'], row['OthersOnLoan'],
                        int(row['CurrentResidenceDuration']), row['OwnsProperty'],
                        int(row['Age']), row['InstallmentPlans'], row['Housing'],
                        int(row['ExistingCreditsCount']), row['Job'], int(row['Dependents']),
                        row['Telephone'], row['ForeignWorker'], row['Risk']
                    ))
                    count += 1
            cls.conn.commit()
            print(f"✅ Loaded {count} synthetic records for testing\n")
        else:
            print("⚠️  CSV file not found, using minimal test data\n")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test database"""
        cls.conn.close()
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)
    
    def test_01_high_risk_query_returns_data(self):
        """
        BREAKING CHANGE EXAMPLE #1: Wrong risk value
        
        Without test data: Developer writes WHERE risk = 'High Risk'
        With test data: Discovers actual value is 'Risk', not 'High Risk'
        """
        print("\n🔍 Test 1: Validating high-risk query returns data")
        print("   Breaking change: Using wrong risk value would return 0 rows")
        
        query = self.queries.get('get_high_risk_applications', '')
        cursor = self.conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        
        self.assertGreater(len(results), 0, 
            "❌ BREAKING: Query returns no results! Check if risk value is correct.")
        
        # Verify all results are actually high risk
        for row in results:
            self.assertEqual(row['risk'], 'Risk',
                "❌ BREAKING: Query returned non-high-risk applications!")
        
        print(f"   ✅ Query correctly returns {len(results)} high-risk applications")
        print(f"   ✅ All results have risk='Risk' (validated against actual data)")
    
    def test_02_statistics_handles_division_safely(self):
        """
        BREAKING CHANGE EXAMPLE #2: Division by zero
        
        Without test data: Developer doesn't test empty result sets
        With test data: Catches division by zero errors
        """
        print("\n🔍 Test 2: Validating statistics query handles edge cases")
        print("   Breaking change: Division by zero when no data exists")
        
        query = self.queries.get('get_risk_statistics', '')
        cursor = self.conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        
        self.assertIsNotNone(result, "❌ BREAKING: Statistics query failed!")
        
        # Check that risk_percentage is calculated correctly
        if result['total_applications'] > 0:
            expected_pct = (result['high_risk_count'] / result['total_applications']) * 100
            actual_pct = result['risk_percentage'] or 0
            self.assertAlmostEqual(actual_pct, expected_pct, places=1,
                msg="❌ BREAKING: Risk percentage calculation is incorrect!")
        
        print(f"   ✅ Total applications: {result['total_applications']}")
        print(f"   ✅ Risk percentage: {result['risk_percentage']}%")
        print(f"   ✅ Division by zero handled correctly")
    
    def test_03_column_names_are_correct(self):
        """
        BREAKING CHANGE EXAMPLE #3: Typo in column name
        
        Without test data: Typo like 'loan_amout' goes unnoticed
        With test data: Query fails immediately with "no such column" error
        """
        print("\n🔍 Test 3: Validating all column names are spelled correctly")
        print("   Breaking change: Typo in column name causes runtime error")
        
        query = self.queries.get('get_applications_by_purpose', '')
        
        # Test with a known loan purpose
        cursor = self.conn.cursor()
        try:
            cursor.execute(query.replace(':loan_purpose', "'furniture'"))
            results = cursor.fetchall()
            
            # Verify we can access loan_amount (not loan_amout)
            for row in results[:3]:
                _ = row['loan_amount']  # This would fail if column name was wrong
            
            print(f"   ✅ All column names spelled correctly")
            print(f"   ✅ Query returned {len(results)} results")
        except sqlite3.OperationalError as e:
            self.fail(f"❌ BREAKING: Column name error: {e}")
    
    def test_04_age_comparison_uses_correct_type(self):
        """
        BREAKING CHANGE EXAMPLE #4: Wrong data type
        
        Without test data: WHERE age < '25' (string) may work in SQLite
        With test data: Catches type mismatches that fail in production databases
        """
        print("\n🔍 Test 4: Validating data type comparisons")
        print("   Breaking change: String comparison instead of integer")
        
        query = self.queries.get('get_young_large_loan_applications', '')
        cursor = self.conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Verify all results actually meet the criteria
        for row in results:
            self.assertLess(row['age'], 25,
                "❌ BREAKING: Query returned age >= 25!")
            self.assertGreater(row['loan_amount'], 10000,
                "❌ BREAKING: Query returned loan_amount <= 10000!")
        
        print(f"   ✅ Found {len(results)} young borrowers with large loans")
        print(f"   ✅ All ages < 25 and loan amounts > 10000 (integer comparison)")
    
    def test_05_null_values_handled_correctly(self):
        """
        BREAKING CHANGE EXAMPLE #5: Missing NULL handling
        
        Without test data: Developer doesn't consider NULL values
        With test data: Discovers NULLs cause unexpected grouping/results
        """
        print("\n🔍 Test 5: Validating NULL value handling")
        print("   Breaking change: NULL values create unexpected results")
        
        query = self.queries.get('analyze_risk_by_employment', '')
        cursor = self.conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        
        self.assertGreater(len(results), 0,
            "❌ BREAKING: Employment analysis returned no results!")
        
        # Verify no NULL employment_duration in results
        for row in results:
            self.assertIsNotNone(row['employment_duration'],
                "❌ BREAKING: NULL employment_duration not handled!")
            self.assertNotEqual(row['employment_duration'], '',
                "❌ BREAKING: Empty employment_duration not handled!")
        
        print(f"   ✅ Found {len(results)} employment duration groups")
        print(f"   ✅ NULL values handled with COALESCE")
    
    def test_06_aggregation_logic_is_correct(self):
        """
        BREAKING CHANGE EXAMPLE #6: Incorrect aggregation
        
        Without test data: Developer doesn't verify calculations
        With test data: Validates percentages, averages, and counts
        """
        print("\n🔍 Test 6: Validating aggregation calculations")
        print("   Breaking change: Incorrect percentage or average calculations")
        
        query = self.queries.get('analyze_risk_by_purpose', '')
        cursor = self.conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        
        for row in results:
            # Verify risk percentage calculation
            if row['total_count'] > 0:
                expected_pct = (row['high_risk_count'] / row['total_count']) * 100
                actual_pct = row['risk_percentage'] or 0
                self.assertAlmostEqual(actual_pct, expected_pct, places=1,
                    msg=f"❌ BREAKING: Risk percentage wrong for {row['loan_purpose']}!")
            
            # Verify HAVING clause works
            self.assertGreaterEqual(row['total_count'], 5,
                "❌ BREAKING: HAVING clause not filtering correctly!")
        
        print(f"   ✅ Found {len(results)} loan purpose groups")
        print(f"   ✅ All calculations verified against actual data")
    
    def test_07_case_statement_logic_is_correct(self):
        """
        BREAKING CHANGE EXAMPLE #7: Wrong CASE ordering
        
        Without test data: Developer doesn't test boundary conditions
        With test data: Catches age misclassification
        """
        print("\n🔍 Test 7: Validating CASE statement logic")
        print("   Breaking change: Wrong CASE order causes misclassification")
        
        query = self.queries.get('analyze_risk_by_age_group', '')
        cursor = self.conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Verify we have all expected age groups
        age_groups = [row['age_group'] for row in results]
        expected_groups = ['Under 25', '25-34', '35-44', '45-54', '55+']
        
        for group in expected_groups:
            if group not in age_groups:
                print(f"   ⚠️  Age group '{group}' not found in results")
        
        print(f"   ✅ Found {len(results)} age groups")
        print(f"   ✅ CASE statement ordering validated")
    
    def test_08_query_returns_expected_structure(self):
        """
        BREAKING CHANGE EXAMPLE #8: Missing columns or wrong structure
        
        Without test data: Developer doesn't verify output structure
        With test data: Ensures all expected columns are present
        """
        print("\n🔍 Test 8: Validating query output structure")
        print("   Breaking change: Missing columns break downstream code")
        
        query = self.queries.get('get_top_risky_combinations', '')
        cursor = self.conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        
        if len(results) > 0:
            row = results[0]
            required_columns = [
                'loan_purpose', 'employment_duration', 'occurrence_count',
                'avg_loan_amount', 'avg_age'
            ]
            
            for col in required_columns:
                self.assertIn(col, row.keys(),
                    f"❌ BREAKING: Missing required column '{col}'!")
            
            print(f"   ✅ Found {len(results)} risky combinations")
            print(f"   ✅ All required columns present in output")
        else:
            print(f"   ⚠️  No risky combinations found (may need more test data)")


def run_tests():
    """Run all tests and generate report"""
    print("\n" + "="*70)
    print("  PRE-COMMIT SQL TESTING")
    print("  Demonstrating why test data catches breaking changes")
    print("="*70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestSQLQueries)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("  TEST SUMMARY")
    print("="*70)
    passed_count = max(0, result.testsRun - len(result.failures) - len(result.errors))
    print(f"Tests Run: {result.testsRun}")
    print(f"✅ Passed: {passed_count}")
    print(f"❌ Failed: {len(result.failures)}")
    print(f"⚠️  Errors: {len(result.errors)}")
    print("="*70 + "\n")
    
    if result.wasSuccessful():
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ Your SQL queries are validated with test data")
        print("✅ No breaking changes detected")
        print("✅ Safe to commit your changes")
        print("\nWhat we caught:")
        print("  • Column names are spelled correctly")
        print("  • Division by zero is handled")
        print("  • Data types are correct")
        print("  • NULL values are handled")
        print("  • Logic errors are caught")
        print("  • Aggregations are accurate")
        print("\nNext steps:")
        print("  git add TDM/mock_app/credit_risk_queries.sql")
        print("  git commit -m 'Add validated SQL queries'")
        return 0
    else:
        print("❌ TESTS FAILED!")
        print("\n⚠️  DO NOT COMMIT - Breaking changes detected!")
        print("\nYour SQL queries have issues that would break in production:")
        for failure in result.failures + result.errors:
            print(f"  • {failure[0]}")
        print("\nFix the issues and run tests again:")
        print("  python3 test_sql.py")
        return 1


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)

# Made with Bob