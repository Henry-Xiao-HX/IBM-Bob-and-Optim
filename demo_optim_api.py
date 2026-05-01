#!/usr/bin/env python3
"""
IBM Optim Archive API Demo Script
For sales demonstrations - showcases key API capabilities
"""

import requests
import json
from typing import Optional
from datetime import datetime
import urllib3
from auth_helper import OptimAuthHelper, load_config_from_env

# Disable SSL warnings for demo environments
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class OptimAPIDemo:
    """Simple demo client for IBM Optim Archive API"""
    
    def __init__(self, base_url: str, access_token: str, account_id: Optional[str] = None):
        """
        Initialize the demo client
        
        Args:
            base_url: API base URL (e.g., 'https://api.example.com')
            access_token: Your API access token
            account_id: Optional account ID for multi-tenant environments
        """
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        if account_id:
            self.headers['account-id'] = account_id
    
    def print_section(self, title: str):
        """Print a formatted section header"""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")
    
    def demo_list_jobs(self):
        """Demo: List all archive jobs"""
        self.print_section("1. LIST ALL ARCHIVE JOBS")
        
        url = f"{self.base_url}/v1/job/savedlist"
        
        print(f"📡 Calling: GET {url}\n")
        
        response = requests.get(url, headers=self.headers, verify=False)
        
        if response.status_code == 200:
            result = response.json()
            
            # Extract jobs from the standard API response format
            jobs = result.get('requestObj', {}).get('resources', [])
            total_count = result.get('requestObj', {}).get('total_count', 0)
            
            print(f"✅ Found {total_count} archive job(s)\n")
            
            if not jobs:
                return None
            
            # Display first 3 jobs
            for i, job in enumerate(jobs[:3], 1):
                print(f"Job {i}:")
                print(f"  • ID: {job.get('id', 'N/A')}")
                print(f"  • Name: {job.get('name', 'N/A')}")
                print(f"  • Status: {job.get('last_run_status', 'N/A')}")
                print(f"  • Created: {job.get('created_at', 'N/A')}")
                print()
            
            return jobs[0].get('id') if jobs else None
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return None
    
    def demo_job_details(self, job_id: str):
        """Demo: Get detailed job information"""
        self.print_section("2. GET JOB DETAILS")
        
        url = f"{self.base_url}/v1/job/details/{job_id}"
        
        print(f"📡 Calling: GET {url}\n")
        
        response = requests.get(url, headers=self.headers, verify=False)
        
        if response.status_code == 200:
            details = response.json()
            print(f"✅ Job Details Retrieved\n")
            print(f"Job Configuration:")
            print(f"  • Name: {details.get('name', 'N/A')}")
            print(f"  • Description: {details.get('description', 'N/A')}")
            print(f"  • Source Connection: {details.get('src_conn_name', 'N/A')}")
            print(f"  • Target Connection: {details.get('dest_conn_name', 'N/A')}")
            print(f"  • Flow ID: {details.get('flow_id', 'N/A')}")
            print()
            return details
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return None
    
    def demo_job_status(self, job_id: str):
        """Demo: Get job execution history"""
        self.print_section("3. GET JOB EXECUTION HISTORY")
        
        url = f"{self.base_url}/v1/job/spark/status/{job_id}"
        params = {'limit': 5}
        
        print(f"📡 Calling: GET {url}")
        print(f"   Parameters: {params}\n")
        
        response = requests.get(url, headers=self.headers, params=params, verify=False)
        
        if response.status_code == 200:
            runs = response.json()
            print(f"✅ Found {len(runs)} recent execution(s)\n")
            
            for i, run in enumerate(runs, 1):
                status_emoji = "✅" if run.get('status') == 'FINISHED' else "⚠️"
                print(f"{status_emoji} Run {i}:")
                print(f"  • Status: {run.get('status', 'N/A')}")
                print(f"  • Started: {run.get('start_time', 'N/A')}")
                print(f"  • Duration: {run.get('duration_seconds', 'N/A')} seconds")
                print(f"  • Spark App ID: {run.get('spark_app_id', 'N/A')}")
                print()
            
            return runs[0].get('spark_app_id') if runs else None
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return None
    
    def demo_archive_schemas(self, job_id: str):
        """Demo: Browse archive schemas"""
        self.print_section("4. BROWSE ARCHIVE SCHEMAS")
        
        url = f"{self.base_url}/v1/file/schemas"
        params = {'id': job_id}
        
        print(f"📡 Calling: GET {url}")
        print(f"   Parameters: {params}\n")
        
        response = requests.get(url, headers=self.headers, params=params, verify=False)
        
        if response.status_code == 200:
            schemas = response.json()
            print(f"✅ Found {len(schemas)} schema(s)\n")
            
            for schema in schemas:
                schema_name = schema.get('name', 'N/A')
                tables = schema.get('tables', [])
                print(f"📁 Schema: {schema_name}")
                print(f"   Tables: {', '.join(tables[:5])}")
                if len(tables) > 5:
                    print(f"   ... and {len(tables) - 5} more")
                print()
            
            # Return first schema and table for next demo
            if schemas and schemas[0].get('tables'):
                return schemas[0].get('name'), schemas[0]['tables'][0]
            return None, None
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return None, None
    
    def demo_table_details(self, job_id: str, schema_name: str, table_name: str):
        """Demo: Get table metadata"""
        self.print_section("5. GET TABLE METADATA")
        
        url = f"{self.base_url}/v1/file/schemas/{schema_name}/tables/{table_name}"
        params = {'id': job_id}
        
        print(f"📡 Calling: GET {url}")
        print(f"   Parameters: {params}\n")
        
        response = requests.get(url, headers=self.headers, params=params, verify=False)
        
        if response.status_code == 200:
            table_info = response.json()
            print(f"✅ Table Metadata Retrieved\n")
            print(f"Table: {schema_name}.{table_name}")
            print(f"  • Row Count: {table_info.get('row_count', 'N/A')}")
            print(f"  • Columns: {len(table_info.get('columns', []))}")
            print(f"  • Last Updated: {table_info.get('last_collection_time', 'N/A')}")
            print(f"\nColumn Details:")
            
            for col in table_info.get('columns', [])[:5]:
                print(f"  • {col.get('name', 'N/A')} ({col.get('type', 'N/A')})")
            
            if len(table_info.get('columns', [])) > 5:
                print(f"  ... and {len(table_info.get('columns', [])) - 5} more columns")
            print()
            return table_info
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return None
    
    def demo_table_data(self, job_id: str, schema_name: str, table_name: str):
        """Demo: Sample archived data"""
        self.print_section("6. SAMPLE ARCHIVED DATA")
        
        url = f"{self.base_url}/v1/file/schemas/{schema_name}/tables/{table_name}/data"
        params = {'id': job_id, 'limit': 3}
        
        print(f"📡 Calling: GET {url}")
        print(f"   Parameters: {params}\n")
        
        response = requests.get(url, headers=self.headers, params=params, verify=False)
        
        if response.status_code == 200:
            data = response.json()
            rows = data.get('rows', [])
            columns = data.get('columns', [])
            
            print(f"✅ Retrieved {len(rows)} sample row(s)\n")
            print(f"Sample Data from {schema_name}.{table_name}:")
            print("-" * 60)
            
            # Print column headers
            col_names = [col.get('name', 'N/A') for col in columns[:5]]
            print(" | ".join(col_names))
            print("-" * 60)
            
            # Print rows
            for row in rows:
                values = [str(row.get(col, 'NULL'))[:20] for col in col_names]
                print(" | ".join(values))
            
            print()
            return data
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return None
    
    def run_full_demo(self):
        """Run complete demo workflow"""
        print("\n" + "="*60)
        print("  IBM OPTIM ARCHIVE API - SALES DEMO")
        print("  Showcasing Key Capabilities")
        print("="*60)
        
        # 1. List jobs
        job_id = self.demo_list_jobs()
        if not job_id:
            print("\n⚠️  No jobs found. Please create an archive job first.")
            return
        
        input("\n👉 Press Enter to continue to job details...")
        
        # 2. Get job details
        self.demo_job_details(job_id)
        
        input("\n👉 Press Enter to continue to execution history...")
        
        # 3. Get execution history
        self.demo_job_status(job_id)
        
        input("\n👉 Press Enter to continue to archive schemas...")
        
        # 4. Browse schemas
        schema_name, table_name = self.demo_archive_schemas(job_id)
        
        if schema_name and table_name:
            input("\n👉 Press Enter to continue to table metadata...")
            
            # 5. Get table details
            self.demo_table_details(job_id, schema_name, table_name)
            
            input("\n👉 Press Enter to continue to data sample...")
            
            # 6. Sample data
            self.demo_table_data(job_id, schema_name, table_name)
        
        self.print_section("DEMO COMPLETE")
        print("✅ Successfully demonstrated all key API capabilities:")
        print("   • Job listing and filtering")
        print("   • Detailed job configuration")
        print("   • Execution history tracking")
        print("   • Schema browsing")
        print("   • Table metadata access")
        print("   • Archived data sampling")
        print("\n💡 All data retrieved via REST API in JSON format")
        print("💡 Perfect for integration with any system or tool")
        print()


def main():
    """Main demo entry point with automatic authentication"""
    print("\n" + "="*60)
    print("  IBM OPTIM ARCHIVE API DEMO SETUP")
    print("="*60 + "\n")
    
    # Try to load configuration from .env file
    config = load_config_from_env()
    
    if config.get('OPTIM_BASE_URL') and config.get('OPTIM_USERNAME') and config.get('OPTIM_PASSWORD'):
        print("✅ Found credentials in .env file\n")
        base_url = config['OPTIM_BASE_URL']
        username = config['OPTIM_USERNAME']
        password = config['OPTIM_PASSWORD']
        account_id = config.get('OPTIM_ACCOUNT_ID', '')
        
        # Check if there's a pre-configured token
        if config.get('OPTIM_ACCESS_TOKEN'):
            print("📋 Using pre-configured access token from .env")
            access_token = config['OPTIM_ACCESS_TOKEN']
        else:
            # Use auth helper to get token (with caching)
            auth = OptimAuthHelper(base_url, username, password)
            access_token = auth.get_access_token()
            
            if not access_token:
                print("\n❌ Failed to retrieve access token!")
                return
    else:
        print("⚠️  No .env file found. Manual configuration required.\n")
        print("Please provide your API credentials:\n")
        
        base_url = input("API Base URL (e.g., https://VM_HOSTNAME:7725/optim): ").strip()
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        account_id = input("Account ID (optional, press Enter to skip): ").strip()
        
        if not all([base_url, username, password]):
            print("\n❌ Error: Base URL, Username, and Password are required!")
            return
        
        # Get access token
        print()
        auth = OptimAuthHelper(base_url, username, password)
        access_token = auth.get_access_token()
        
        if not access_token:
            print("\n❌ Failed to retrieve access token!")
            return
    
    print()
    
    # Create demo client
    demo = OptimAPIDemo(
        base_url=base_url,
        access_token=access_token,
        account_id=account_id if account_id else None
    )
    
    # Run the demo
    demo.run_full_demo()


if __name__ == "__main__":
    main()

# Made with Bob
