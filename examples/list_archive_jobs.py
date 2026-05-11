#!/usr/bin/env python3
"""
Example: List Archive Jobs

This example demonstrates how to retrieve and display all archive jobs
from the IBM Optim Archive API.
"""

import sys
from pathlib import Path
import requests
import urllib3

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from auth_helper import OptimAuthHelper, load_config_from_env

# Disable SSL warnings for demo environments
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def list_archive_jobs(base_url: str, access_token: str):
    """
    List all archive jobs
    
    Args:
        base_url: API base URL
        access_token: Valid access token
        
    Returns:
        List of jobs or None if error
    """
    url = f"{base_url}/v1/job/savedlist"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            jobs = data.get('requestObj', {}).get('jobs', [])
            return jobs
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return None


def main():
    """Main example function"""
    print("=" * 60)
    print("Example: List Archive Jobs")
    print("=" * 60)
    
    # Load configuration
    config = load_config_from_env()
    
    if not all([config.get('OPTIM_BASE_URL'), 
                config.get('OPTIM_USERNAME'), 
                config.get('OPTIM_PASSWORD')]):
        print("\n❌ Error: Missing required configuration in .env file")
        return
    
    # Authenticate
    print("\n1. Authenticating...")
    auth = OptimAuthHelper(
        base_url=config['OPTIM_BASE_URL'],
        username=config['OPTIM_USERNAME'],
        password=config['OPTIM_PASSWORD']
    )
    
    token = auth.get_access_token()
    if not token:
        print("❌ Authentication failed")
        return
    
    # List jobs
    print("\n2. Fetching archive jobs...")
    jobs = list_archive_jobs(config['OPTIM_BASE_URL'], token)
    
    if jobs:
        print(f"\n✅ Found {len(jobs)} archive job(s)\n")
        print("-" * 60)
        
        for idx, job in enumerate(jobs, 1):
            job_id = job.get('id', 'N/A')
            job_name = job.get('name', 'N/A')
            description = job.get('description', 'No description')
            
            print(f"{idx}. Job ID: {job_id}")
            print(f"   Name: {job_name}")
            print(f"   Description: {description}")
            print("-" * 60)
    else:
        print("\n⚠️  No jobs found or error occurred")


if __name__ == "__main__":
    main()
