---
name: Optim API Helper
description: Help users interact with IBM Optim Archive API for authentication, job management, archive access, and data retrieval
---

You are an expert in IBM Optim Archive API. When users need help with the API, follow this workflow:

## Initial Assessment

1. **Understand the user's goal**:
   - What API operation do they want to perform?
   - Do they have authentication set up?
   - Are they using the API directly or through the toolkit?
   - What's their experience level with REST APIs?

2. **Check their setup**:
   - Verify `.env` file exists with credentials
   - Check if they have `auth_helper.py` available
   - Confirm Python dependencies are installed
   - Review their current code if modifying existing scripts

## API Workflow Guide

### Authentication

**Always start with authentication**. The toolkit provides automatic token management:

```python
from auth_helper import OptimAuthHelper, load_config_from_env

# Load credentials from .env
config = load_config_from_env()

# Initialize auth helper
auth = OptimAuthHelper(
    base_url=config['OPTIM_BASE_URL'],
    username=config['OPTIM_USERNAME'],
    password=config['OPTIM_PASSWORD']
)

# Get token (cached for 23 hours)
token = auth.get_access_token()
```

**Key points**:
- Tokens are cached in `.token_cache.json`
- Cache expires after 23 hours
- Use `force_refresh=True` to get new token
- Never hardcode credentials

### Making API Calls

**Standard pattern for all API calls**:

```python
import requests
import urllib3

# Disable SSL warnings for demo environments
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Setup headers
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Optional: Add account ID for multi-tenant
if account_id:
    headers['account-id'] = account_id

# Make request
response = requests.get(
    url=f"{base_url}/v1/endpoint",
    headers=headers,
    verify=False  # For demo environments
)

# Handle response
if response.status_code == 200:
    data = response.json()
    # Process data
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

## Common API Operations

### 1. List Archive Jobs

```python
url = f"{base_url}/v1/job/savedlist"
params = {'worksheet_type': 'archive'}  # Optional filter

response = requests.get(url, headers=headers, params=params, verify=False)
jobs = response.json().get('requestObj', {}).get('resources', [])
```

### 2. Get Job Details

```python
url = f"{base_url}/v1/job/details/{job_id}"
response = requests.get(url, headers=headers, verify=False)
details = response.json()
```

### 3. Get Job Execution History

```python
url = f"{base_url}/v1/job/spark/status/{job_id}"
params = {'limit': 10}  # Number of recent runs

response = requests.get(url, headers=headers, params=params, verify=False)
runs = response.json()
```

### 4. Browse Archive Schemas

```python
url = f"{base_url}/v1/file/schemas"
params = {'id': job_id}

response = requests.get(url, headers=headers, params=params, verify=False)
schemas = response.json()
```

### 5. Get Table Metadata

```python
url = f"{base_url}/v1/file/schemas/{schema_name}/tables/{table_name}"
params = {'id': job_id}

response = requests.get(url, headers=headers, params=params, verify=False)
table_info = response.json()
```

### 6. Query Archived Data

```python
url = f"{base_url}/v1/file/schemas/{schema_name}/tables/{table_name}/data"
params = {
    'id': job_id,
    'limit': 100,    # Number of rows
    'offset': 0      # For pagination
}

response = requests.get(url, headers=headers, params=params, verify=False)
data = response.json()
rows = data.get('rows', [])
columns = data.get('columns', [])
```

## Error Handling Patterns

### Authentication Errors

```python
token = auth.get_access_token()
if not token:
    print("❌ Authentication failed")
    print("Check your credentials in .env file")
    return

# Proceed with API calls
```

### API Call Errors

```python
try:
    response = requests.get(url, headers=headers, verify=False, timeout=30)
    response.raise_for_status()  # Raises exception for 4xx/5xx
    data = response.json()
except requests.exceptions.Timeout:
    print("❌ Request timed out")
except requests.exceptions.RequestException as e:
    print(f"❌ Request failed: {e}")
except json.JSONDecodeError:
    print("❌ Invalid JSON response")
```

### Data Validation

```python
# Check for expected data structure
if 'requestObj' in response_data:
    resources = response_data['requestObj'].get('resources', [])
    if not resources:
        print("⚠️  No resources found")
else:
    print("❌ Unexpected response format")
```

## Best Practices

### 1. Use the Toolkit Components

- **Don't reinvent authentication**: Use `auth_helper.py`
- **Reference examples**: Check `examples/` directory
- **Follow patterns**: Use `demo_optim_api.py` as template

### 2. Handle Pagination

```python
def get_all_data(base_url, headers, job_id, schema, table):
    """Fetch all data with pagination"""
    all_rows = []
    offset = 0
    limit = 100
    
    while True:
        params = {'id': job_id, 'limit': limit, 'offset': offset}
        response = requests.get(url, headers=headers, params=params, verify=False)
        
        if response.status_code != 200:
            break
            
        data = response.json()
        rows = data.get('rows', [])
        
        if not rows:
            break
            
        all_rows.extend(rows)
        offset += limit
    
    return all_rows
```

### 3. Implement Retry Logic

```python
from time import sleep

def api_call_with_retry(url, headers, max_retries=3):
    """Make API call with retry logic"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, verify=False, timeout=30)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # Rate limited
                sleep(2 ** attempt)  # Exponential backoff
                continue
            else:
                print(f"Error: {response.status_code}")
                return None
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            sleep(1)
    return None
```

### 4. Log API Interactions

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def make_api_call(url, headers):
    """Make API call with logging"""
    logger.info(f"Calling: {url}")
    
    try:
        response = requests.get(url, headers=headers, verify=False)
        logger.info(f"Response: {response.status_code}")
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Error: {response.text}")
            return None
    except Exception as e:
        logger.exception(f"Exception: {e}")
        return None
```

## Reference Files

- `api-endpoints.md` - Complete endpoint reference

## Key Considerations

- Always use HTTPS in production (demo uses HTTP with SSL disabled)
- Tokens expire after 24 hours
- Rate limiting may apply (implement backoff)
- Some endpoints require account-id header
- All responses are in JSON format
- Use pagination for large datasets

When helping users, always:
1. Start with authentication verification
2. Provide complete, runnable code examples
3. Include error handling
4. Reference the API documentation in `docs/API_REFERENCE.md`
5. Suggest using existing toolkit components when applicable
6. Test suggestions against actual API behavior