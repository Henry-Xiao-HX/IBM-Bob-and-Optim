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

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

print("Testing different ways to list jobs:\n")

# Test 1: Without worksheet_type parameter
print("=" * 60)
print("Test 1: GET /v1/job/savedlist (no parameters)")
print("=" * 60)
url = f"{base_url}/v1/job/savedlist"
response = requests.get(url, headers=headers, verify=False)
print(f"Status: {response.status_code}")
print(json.dumps(response.json(), indent=2))

# Test 2: With worksheet_type=archive
print("\n" + "=" * 60)
print("Test 2: GET /v1/job/savedlist?worksheet_type=archive")
print("=" * 60)
response = requests.get(url, headers=headers, params={'worksheet_type': 'archive'}, verify=False)
print(f"Status: {response.status_code}")
print(json.dumps(response.json(), indent=2))

# Test 3: Try listing all jobs (different endpoint if exists)
print("\n" + "=" * 60)
print("Test 3: GET /v1/job/list")
print("=" * 60)
url = f"{base_url}/v1/job/list"
response = requests.get(url, headers=headers, verify=False)
print(f"Status: {response.status_code}")
print(json.dumps(response.json(), indent=2))

# Made with Bob
