#!/usr/bin/env python3
"""
IBM Optim Archive API Demo Script - Auto Mode
Runs through all demo steps automatically without user prompts
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
            result = response.json()
            runs = result.get('requestObj', {}).get('spark_runs', [])
            print(f"✅ Found {len(runs)} recent execution(s)\n")
            
            for i, run in enumerate(runs, 1):
                status_emoji = "✅" if run.get('status') == 'FINISHED' else "⚠️"
                duration_ms = run.get('duration_ms', 0)
                duration_sec = duration_ms / 1000 if duration_ms else 0
                print(f"{status_emoji} Run {i}:")
                print(f"  • Status: {run.get('status', 'N/A')}")
                print(f"  • Started: {run.get('start_time', 'N/A')}")
                print(f"  • Duration: {duration_sec:.2f} seconds")
                print(f"  • Spark App ID: {run.get('spark_app_id', 'N/A')}")
                print()
            
            return runs[0].get('spark_app_id') if runs else None
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return None
    
    def demo_list_archives(self):
        """Demo: List all archive files"""
        self.print_section("4. LIST ARCHIVE FILES")
        
        url = f"{self.base_url}/v1/file/savedlist"
        
        print(f"📡 Calling: GET {url}\n")
        
        response = requests.get(url, headers=self.headers, verify=False)
        
        if response.status_code == 200:
            result = response.json()
            archives = result.get('requestObj', {}).get('resources', [])
            total_count = result.get('requestObj', {}).get('total_count', 0)
            
            print(f"✅ Found {total_count} archive file(s)\n")
            
            if not archives:
                print("⚠️  No archive files found. Archives are created when jobs complete successfully.")
                return None
            
            # Display first 3 archives
            for i, archive in enumerate(archives[:3], 1):
                print(f"Archive {i}:")
                print(f"  • ID: {archive.get('id', 'N/A')}")
                print(f"  • Name: {archive.get('name', 'N/A')}")
                print(f"  • Job ID: {archive.get('job_id', 'N/A')}")
                print(f"  • Created: {archive.get('created_at', 'N/A')}")
                print()
            
            return archives[0].get('id') if archives else None
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return None
    
    def demo_archive_schemas(self, archive_id: str):
        """Demo: Browse archive schemas"""
        self.print_section("5. BROWSE ARCHIVE SCHEMAS")
        
        url = f"{self.base_url}/v1/file/schemas"
        params = {'id': archive_id}
        
        print(f"📡 Calling: GET {url}")
        print(f"   Parameters: {params}\n")
        
        response = requests.get(url, headers=self.headers, params=params, verify=False)
        
        if response.status_code == 200:
            result = response.json()
            
            # Handle different response formats
            if isinstance(result, dict):
                # Response is wrapped in an object
                schemas = result.get('schemas', [])
            elif isinstance(result, list):
                # Response is a direct list
                schemas = result
            else:
                print(f"⚠️  Unexpected response format")
                return None, None
            
            print(f"✅ Found {len(schemas)} schema(s)\n")
            
            # Schemas might be objects or strings
            for schema in schemas:
                if isinstance(schema, dict):
                    schema_name = schema.get('name', 'N/A')
                    tables = schema.get('tables', [])
                    print(f"📁 Schema: {schema_name}")
                    print(f"   Tables: {', '.join(tables[:5])}")
                    if len(tables) > 5:
                        print(f"   ... and {len(tables) - 5} more")
                elif isinstance(schema, str):
                    # Schema is just a string name, need to fetch tables separately
                    print(f"📁 Schema: {schema}")
                    print(f"   (Use table listing endpoint to see tables)")
                print()
            
            # Return first schema for next demo
            if schemas:
                if isinstance(schemas[0], dict):
                    schema_name = schemas[0].get('name')
                    tables = schemas[0].get('tables', [])
                    if tables:
                        return schema_name, tables[0]
                elif isinstance(schemas[0], str):
                    # Just return the schema name, we'll need to list tables
                    return schemas[0], None
            
            return None, None
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return None, None
    
    def demo_list_tables(self, archive_id: str, schema_name: str):
        """Demo: List tables in a schema"""
        self.print_section("6. LIST TABLES IN SCHEMA")
        
        url = f"{self.base_url}/v1/file/schemas/{schema_name}/tables"
        params = {'id': archive_id}
        
        print(f"📡 Calling: GET {url}")
        print(f"   Parameters: {params}\n")
        
        response = requests.get(url, headers=self.headers, params=params, verify=False)
        
        if response.status_code == 200:
            tables = response.json()
            print(f"✅ Found {len(tables)} table(s) in schema '{schema_name}'\n")
            
            for i, table in enumerate(tables[:10], 1):
                if isinstance(table, dict):
                    print(f"  {i}. {table.get('name', 'N/A')}")
                else:
                    print(f"  {i}. {table}")
            
            if len(tables) > 10:
                print(f"  ... and {len(tables) - 10} more tables")
            print()
            
            # Return first table name
            if tables:
                if isinstance(tables[0], dict):
                    return tables[0].get('name')
                else:
                    return tables[0]
            return None
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return None
    
    def demo_table_details(self, archive_id: str, schema_name: str, table_name: str):
        """Demo: Get table metadata"""
        self.print_section("6. GET TABLE METADATA")
        
        url = f"{self.base_url}/v1/file/schemas/{schema_name}/tables/{table_name}"
        params = {'id': archive_id}
        
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
    
    def demo_table_data(self, archive_id: str, schema_name: str, table_name: str):
        """Demo: Sample archived data"""
        self.print_section("8. SAMPLE ARCHIVED DATA")
        
        url = f"{self.base_url}/v1/file/schemas/{schema_name}/tables/{table_name}/data"
        params = {'id': archive_id, 'limit': 3}
        
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
        """Run complete demo workflow automatically"""
        print("\n" + "="*60)
        print("  IBM OPTIM ARCHIVE API - SALES DEMO (AUTO MODE)")
        print("  Showcasing Key Capabilities")
        print("="*60)
        
        # 1. List jobs
        job_id = self.demo_list_jobs()
        if not job_id:
            print("\n⚠️  No jobs found. Please create an archive job first.")
            return
        
        # 2. Get job details
        self.demo_job_details(job_id)
        
        # 3. Get execution history
        self.demo_job_status(job_id)
        
        # 4. List archive files
        archive_id = self.demo_list_archives()
        
        if not archive_id:
            print("\n⚠️  No archive files found.")
            print("💡 Archive files are created when jobs complete successfully.")
            print("💡 Please run an archive job first, then try this demo again.")
            return
        
        # 5. Browse schemas
        schema_name, table_name = self.demo_archive_schemas(archive_id)
        
        if not schema_name:
            print("\n⚠️  No schemas found in archive.")
            return
        
        # 6. List tables if we don't have a table name yet
        if not table_name:
            table_name = self.demo_list_tables(archive_id, schema_name)
        
        if schema_name and table_name:
            # 7. Get table details
            self.demo_table_details(archive_id, schema_name, table_name)
            
            # 8. Sample data
            self.demo_table_data(archive_id, schema_name, table_name)
        
        self.print_section("DEMO COMPLETE")
        print("✅ Successfully demonstrated all key API capabilities:")
        print("   • Job listing and filtering")
        print("   • Detailed job configuration")
        print("   • Execution history tracking")
        print("   • Archive file listing")
        print("   • Schema browsing")
        print("   • Table listing")
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
