#!/usr/bin/env python3
"""
Credit Risk Assessment Application
Demonstrates testing with synthetic data from Optim before committing changes

PRE-COMMIT TESTING WORKFLOW:
This file is monitored by a Git pre-commit hook. Whenever you commit changes to this file,
the test suite (test_app.py) automatically runs with synthetic data from Optim Archive.

How it works:
1. You modify this file (app.py)
2. You stage changes: git add TDM/mock_app/app.py
3. You commit: git commit -m "Your message"
4. Pre-commit hook automatically runs test_app.py
5. If tests pass → commit proceeds
6. If tests fail → commit is blocked until you fix the issues

Manual testing before commit:
  cd TDM/mock_app && ./run_tests.sh

See README.md for full documentation on the automated testing workflow.
"""

import csv
import sqlite3
from typing import List, Dict, Optional
from pathlib import Path


class CreditRiskDatabase:
    """Credit risk assessment database for testing"""
    
    def __init__(self, db_path: str = "credit_risk.db"):
        self.db_path = db_path
        self.conn = None
        self.setup_database()
    
    def setup_database(self):
        """Initialize database schema"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()
        
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
                risk VARCHAR(20),
                predicted_label VARCHAR(20),
                probability VARCHAR(20)
            )
        """)
        
        self.conn.commit()
    
    def load_test_data_from_csv(self, csv_file: str, limit: int = 1000):
        """Load test data from CSV file"""
        cursor = self.conn.cursor()
        count = 0
        
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if count >= limit:
                    break
                
                cursor.execute("""
                    INSERT INTO credit_applications 
                    (checking_status, loan_duration, credit_history, loan_purpose, 
                     loan_amount, existing_savings, employment_duration, installment_percent,
                     sex, others_on_loan, current_residence_duration, owns_property,
                     age, installment_plans, housing, existing_credits_count,
                     job, dependents, telephone, foreign_worker, risk, predicted_label, probability)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    row['CheckingStatus'], int(row['LoanDuration']), row['CreditHistory'],
                    row['LoanPurpose'], int(row['LoanAmount']), row['ExistingSavings'],
                    row['EmploymentDuration'], int(row['InstallmentPercent']),
                    row['Sex'], row['OthersOnLoan'], int(row['CurrentResidenceDuration']),
                    row['OwnsProperty'], int(row['Age']), row['InstallmentPlans'],
                    row['Housing'], int(row['ExistingCreditsCount']), row['Job'],
                    int(row['Dependents']), row['Telephone'], row['ForeignWorker'],
                    row['Risk'], row['predicted_label'], row['probability']
                ))
                count += 1
        
        self.conn.commit()
        return count
    
    def get_application(self, app_id: int) -> Optional[Dict]:
        """Get credit application by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM credit_applications WHERE id = ?", (app_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_high_risk_applications(self) -> List[Dict]:
        """Get all high-risk applications"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM credit_applications WHERE risk = 'Risk'")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_applications_by_purpose(self, purpose: str) -> List[Dict]:
        """Get applications by loan purpose"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM credit_applications WHERE loan_purpose = ? LIMIT 10",
            (purpose,)
        )
        return [dict(row) for row in cursor.fetchall()]
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as total FROM credit_applications")
        total = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as high_risk FROM credit_applications WHERE risk = 'Risk'")
        high_risk = cursor.fetchone()['high_risk']
        
        cursor.execute("SELECT AVG(loan_amount) as avg_loan FROM credit_applications")
        avg_loan = cursor.fetchone()['avg_loan']
        
        cursor.execute("SELECT AVG(age) as avg_age FROM credit_applications")
        avg_age = cursor.fetchone()['avg_age']
        
        return {
            'total_applications': total,
            'high_risk_count': high_risk,
            'low_risk_count': total - high_risk,
            'risk_percentage': (high_risk / total * 100) if total > 0 else 0,
            'average_loan_amount': avg_loan,
            'average_age': avg_age
        }
    
    def assess_risk(self, loan_amount: int, age: int, employment_duration: str) -> str:
        """
        Simple risk assessment logic (this is what we're testing!)
        NEW FEATURE: Enhanced risk assessment with employment duration
        """
        risk_score = 0
        
        # Loan amount risk
        if loan_amount > 10000:
            risk_score += 2
        elif loan_amount > 5000:
            risk_score += 1
        
        # Age risk
        if age < 25:
            risk_score += 2
        elif age < 35:
            risk_score += 1
        
        # Employment duration risk (NEW LOGIC)
        if employment_duration == 'less_1':
            risk_score += 3
        elif employment_duration in ['1_to_4', '4_to_7']:
            risk_score += 1
        
        # Risk determination
        if risk_score >= 4:
            return 'High Risk'
        elif risk_score >= 2:
            return 'Medium Risk'
        else:
            return 'Low Risk'
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


def main():
    """Demo application"""
    print("\n" + "="*70)
    print("  CREDIT RISK ASSESSMENT APPLICATION")
    print("  Testing with Synthetic Data from Optim")
    print("="*70 + "\n")
    
    # Initialize database
    db = CreditRiskDatabase()
    
    # Load test data
    print("📊 Loading synthetic test data from CSV...")
    csv_file = 'credit_risk_mock_data.csv'
    
    if not Path(csv_file).exists():
        print(f"❌ Error: {csv_file} not found!")
        print("   This file should contain synthetic credit risk data from Optim")
        return
    
    try:
        count = db.load_test_data_from_csv(csv_file, limit=1000)
        print(f"✅ Loaded {count} credit applications for testing\n")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return
    
    # Show statistics
    stats = db.get_statistics()
    print("📈 Database Statistics:")
    print(f"   • Total Applications: {stats['total_applications']}")
    print(f"   • High Risk: {stats['high_risk_count']} ({stats['risk_percentage']:.1f}%)")
    print(f"   • Low Risk: {stats['low_risk_count']}")
    print(f"   • Average Loan Amount: ${stats['average_loan_amount']:.2f}")
    print(f"   • Average Age: {stats['average_age']:.1f} years")
    print()
    
    # Demo operations
    print("🔍 Testing Application Features:\n")
    
    # 1. Get application by ID
    print("1. Get Credit Application by ID (id=1):")
    app = db.get_application(1)
    if app:
        print(f"   ✅ Found application:")
        print(f"      • Loan Amount: ${app['loan_amount']}")
        print(f"      • Purpose: {app['loan_purpose']}")
        print(f"      • Risk: {app['risk']}")
        print(f"      • Age: {app['age']}")
    print()
    
    # 2. Get high-risk applications
    print("2. Get High-Risk Applications:")
    high_risk = db.get_high_risk_applications()
    print(f"   ✅ Found {len(high_risk)} high-risk application(s)")
    for app in high_risk[:3]:
        print(f"      • ID {app['id']}: ${app['loan_amount']} - {app['loan_purpose']}")
    print()
    
    # 3. Search by purpose
    print("3. Get Applications by Purpose (furniture):")
    furniture_apps = db.get_applications_by_purpose('furniture')
    print(f"   ✅ Found {len(furniture_apps)} furniture loan(s)")
    print()
    
    # 4. Test NEW risk assessment logic
    print("4. Test NEW Risk Assessment Logic:")
    test_cases = [
        (5000, 30, 'greater_7', 'Low loan, good age, stable employment'),
        (12000, 22, 'less_1', 'High loan, young, new employment'),
        (8000, 40, '4_to_7', 'Medium loan, mature, moderate employment')
    ]
    
    for loan, age, employment, description in test_cases:
        risk = db.assess_risk(loan, age, employment)
        print(f"   • {description}")
        print(f"     Loan: ${loan}, Age: {age}, Employment: {employment}")
        print(f"     → Risk Assessment: {risk}")
    print()
    
    print("="*70)
    print("✅ All features tested successfully with synthetic data!")
    print("="*70 + "\n")
    
    db.close()


if __name__ == "__main__":
    main()

# Made with Bob
