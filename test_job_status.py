#!/usr/bin/env python3
import requests
import json
import urllib3
from auth_helper import OptimAuthHelper, load_config_from_env

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load config
config = load_config_from_env()
base_url = config['OPTIM_BASE_URL']
username = config['OPTIM_USERNAME']
password = config['OPTIM_PASSWORD']

# Get token
auth = OptimAuthHelper(base_url, username, password)
access_token = auth.get_access_token()

# Get job ID
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# First get a job ID
url = f"{base_url}/v1/job/savedlist"
response = requests.get(url, headers=headers, verify=False)
jobs = response.json().get('requestObj', {}).get('resources', [])
job_id = jobs[0]['id'] if jobs else None

if job_id:
    print(f"Testing job status for: {job_id}\n")
    
    # Test job status endpoint
    url = f"{base_url}/v1/job/spark/status/{job_id}"
    params = {'limit': 5}
    
    response = requests.get(url, headers=headers, params=params, verify=False)
    
    print(f"Status Code: {response.status_code}")
    print(f"\nRaw Response:")
    print(response.text)
    print(f"\nParsed JSON:")
    print(json.dumps(response.json(), indent=2))
else:
    print("No jobs found")

# Made with Bob
