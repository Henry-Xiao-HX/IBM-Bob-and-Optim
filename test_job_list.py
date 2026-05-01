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

# Make request
url = f"{base_url}/v1/job/savedlist"
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}
params = {'worksheet_type': 'archive'}

response = requests.get(url, headers=headers, params=params, verify=False)

print(f"Status Code: {response.status_code}")
print(f"\nRaw Response:")
print(response.text)
print(f"\nParsed JSON:")
print(json.dumps(response.json(), indent=2))

# Made with Bob
