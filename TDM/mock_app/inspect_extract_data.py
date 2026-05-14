#!/usr/bin/env python3
"""
Inspect the actual data structure in Optim database tables
"""

import os
import sys
from pathlib import Path
import json
from urllib.parse import quote

# Add parent directories to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, grandparent_dir)
sys.path.insert(0, parent_dir)

from auth_helper import OptimAuthHelper
import requests

def load_config_from_root_env():
    """Load configuration from root .env file"""
    config = {}
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

def list_connection_profiles(base_url, headers):
    """List all available connection profiles"""
    print("📋 Fetching connection profiles...")
    url = f"{base_url}/v1/connprofiles"
    response = requests.get(url, headers=headers, verify=False)
    
    if response.status_code != 200:
        print(f"❌ Failed to get connection profiles: HTTP {response.status_code}")
        print(f"   Response: {response.text}")
        return []
    
    response_data = response.json()
    
    # Extract profiles from the response structure
    profiles_list = []
    
    # Handle the actual API response structure
    if isinstance(response_data, dict):
        request_obj = response_data.get('requestObj', {})
        infos = request_obj.get('infos', [])
        
        if infos:
            print(f"✅ Found {len(infos)} connection profile(s):\n")
            
            for i, info in enumerate(infos, 1):
                connection = info.get('connection', {})
                profile_name = connection.get('name', 'Unknown')
                properties = connection.get('properties', {})
                
                profile_type = properties.get('type', 'Unknown')
                profile_host = properties.get('host', 'N/A')
                profile_db = properties.get('database', 'N/A')
                profile_desc = properties.get('description', '')
                
                print(f"   {i}. {profile_name}")
                print(f"      Type: {profile_type}")
                print(f"      Host: {profile_host}")
                print(f"      Database: {profile_db}")
                if profile_desc:
                    print(f"      Description: {profile_desc}")
                print()
                
                # Store profile with name and properties
                profiles_list.append({
                    'name': profile_name,
                    'type': profile_type,
                    'host': profile_host,
                    'database': profile_db,
                    'properties': properties
                })
            
            return profiles_list
    
    # Fallback for other response formats
    if isinstance(response_data, list):
        print(f"✅ Found {len(response_data)} connection profile(s):\n")
        for i, profile in enumerate(response_data, 1):
            if isinstance(profile, str):
                print(f"   {i}. {profile}")
                profiles_list.append({'name': profile})
            else:
                profile_name = profile.get('name', 'Unknown')
                print(f"   {i}. {profile_name}")
                profiles_list.append(profile)
        print()
        return profiles_list
    
    return []

def inspect_connection_data(base_url, headers, conn_profile_name, schema_name=None, table_name=None):
    """Inspect data from a specific connection profile"""
    print(f"\n{'='*70}")
    print(f"  INSPECTING CONNECTION: {conn_profile_name}")
    print(f"{'='*70}\n")
    
    # Update headers with connection profile
    conn_headers = headers.copy()
    conn_headers['optim-conn-profile'] = conn_profile_name
    
    # List schemas
    print("📡 Fetching schemas...")
    url = f"{base_url}/v1/database/schemas"
    params = {'limit': 100, 'show_systems': 'true'}  # Include system schemas
    response = requests.get(url, headers=conn_headers, params=params, verify=False)
    
    if response.status_code != 200:
        print(f"❌ Failed to get schemas: HTTP {response.status_code}")
        print(f"   Response: {response.text}")
        return False
    
    schemas_data = response.json()
    
    # Handle different response formats
    schemas = []
    if isinstance(schemas_data, dict):
        # Try multiple possible paths in the response
        request_obj = schemas_data.get('requestObj', {})
        
        # Check for 'resources' array (DB2 format)
        if 'resources' in request_obj:
            schemas = request_obj['resources']
        # Check for 'schemas' array
        elif 'schemas' in request_obj:
            schemas = request_obj['schemas']
        # Check for 'infos' array
        elif 'infos' in request_obj:
            schemas = request_obj['infos']
            # If infos format, extract schema names
            if schemas and isinstance(schemas, list) and len(schemas) > 0:
                if isinstance(schemas[0], dict) and 'schema' in schemas[0]:
                    schemas = [item.get('schema', {}) for item in schemas]
        # Check top-level 'schemas'
        elif 'schemas' in schemas_data:
            schemas = schemas_data['schemas']
    elif isinstance(schemas_data, list):
        schemas = schemas_data
    
    print(f"✅ Found {len(schemas)} schema(s)")
    
    if not schemas:
        print("   No schemas available")
        return True
    
    # Use provided schema or first available
    target_schema = schema_name if schema_name else schemas[0].get('name')
    print(f"   Using schema: {target_schema}\n")
    
    # List tables in schema
    print(f"📡 Fetching tables in schema '{target_schema}'...")
    url = f"{base_url}/v1/database/schemas/{target_schema}/tables"
    params = {'limit': 50}
    response = requests.get(url, headers=conn_headers, params=params, verify=False)
    
    if response.status_code != 200:
        print(f"❌ Failed to get tables: HTTP {response.status_code}")
        print(f"   Response: {response.text}")
        return False
    
    tables_data = response.json()
    
    # Debug: Print the actual response structure
    print(f"   DEBUG - Response structure: {json.dumps(tables_data, indent=2)[:500]}...")
    
    # Handle different response formats (similar to schemas)
    tables = []
    if isinstance(tables_data, dict):
        # Try multiple possible paths in the response
        request_obj = tables_data.get('requestObj', {})
        
        # Check for 'resources' array (DB2 format)
        if 'resources' in request_obj:
            tables = request_obj['resources']
        # Check for 'tables' array in requestObj
        elif 'tables' in request_obj:
            tables = request_obj['tables']
        # Check for 'infos' array
        elif 'infos' in request_obj:
            tables = request_obj['infos']
            # If infos format, extract table objects
            if tables and isinstance(tables, list) and len(tables) > 0:
                if isinstance(tables[0], dict) and 'table' in tables[0]:
                    tables = [item.get('table', {}) for item in tables]
        # Check top-level 'tables'
        elif 'tables' in tables_data:
            tables = tables_data['tables']
    elif isinstance(tables_data, list):
        tables = tables_data
    
    print(f"✅ Found {len(tables)} table(s)")
    
    if not tables:
        print("   No tables available")
        return True
    
    # Show first few tables
    print(f"   Tables (showing first 10):")
    for i, table in enumerate(tables[:10], 1):
        table_name_str = table.get('name', 'Unknown')
        row_count = table.get('row_count', 'N/A')
        print(f"      {i}. {table_name_str} ({row_count} rows)")
    if len(tables) > 10:
        print(f"      ... and {len(tables) - 10} more tables")
    print()
    
    # Use provided table or first available
    target_table = table_name if table_name else tables[0].get('name')
    print(f"📋 Inspecting table: {target_schema}.{target_table}\n")
    
    # Get table metadata
    print("📡 Fetching table metadata...")
    # URL-encode the table name to handle special characters
    encoded_table = quote(target_table, safe='')
    url = f"{base_url}/v1/database/schemas/{target_schema}/tables/{encoded_table}"
    response = requests.get(url, headers=conn_headers, verify=False)
    
    if response.status_code != 200:
        print(f"❌ Failed to get table info: HTTP {response.status_code}")
        print(f"   Response: {response.text}")
        return False
    
    table_info = response.json()
    
    # Debug: Print the actual table info structure
    print(f"   DEBUG - Table metadata response:")
    print(f"   {json.dumps(table_info, indent=2)}")
    
    columns = table_info.get('columns', [])
    
    # Try alternative paths for columns
    if not columns and isinstance(table_info, dict):
        request_obj = table_info.get('requestObj', {})
        if 'columns' in request_obj:
            columns = request_obj['columns']
        elif 'table' in request_obj:
            table_obj = request_obj.get('table', {})
            if 'columns' in table_obj:
                columns = table_obj['columns']
    
    print(f"✅ Table metadata retrieved")
    print(f"   Columns ({len(columns)}):")
    for col in columns[:10]:
        print(f"      - {col.get('name')} ({col.get('type')})")
    if len(columns) > 10:
        print(f"      ... and {len(columns) - 10} more columns")
    print()
    
    # Get sample data
    print("📡 Fetching sample data...")
    # URL-encode the table name to handle special characters
    encoded_table = quote(target_table, safe='')
    url = f"{base_url}/v1/database/schemas/{target_schema}/tables/{encoded_table}/data"
    params = {'limit': 3}
    response = requests.get(url, headers=conn_headers, params=params, verify=False)
    
    if response.status_code != 200:
        print(f"❌ Failed to get table data: HTTP {response.status_code}")
        print(f"   Response: {response.text}")
        return False
    
    data_result = response.json()
    
    # Debug: Print the actual data response structure
    print(f"   DEBUG - Data response:")
    print(f"   {json.dumps(data_result, indent=2)}")
    
    rows = data_result.get('rows', [])
    
    # Try alternative paths for rows
    if not rows and isinstance(data_result, dict):
        request_obj = data_result.get('requestObj', {})
        if 'rows' in request_obj:
            rows = request_obj['rows']
        elif 'resources' in request_obj:
            rows = request_obj['resources']
    
    print(f"✅ Sample data retrieved ({len(rows)} rows):")
    if rows:
        if len(rows) > 0 and len(columns) > 0:
            first_row = rows[0]
            print(f"\n   First row structure:")
            for i, col in enumerate(columns[:10]):
                value = first_row[i] if i < len(first_row) else 'N/A'
                print(f"      {col.get('name')}: {value}")
            if len(columns) > 10:
                print(f"      ... and {len(columns) - 10} more fields")
    else:
        print("   ⚠️  No rows returned")
    
    print()
    return True

def main():
    print("="*70)
    print("  INSPECTING OPTIM DATABASE DATA FROM CONNECTIONS")
    print("="*70 + "\n")
    
    # Load configuration
    config = load_config_from_root_env()
    
    if not all([config.get('OPTIM_BASE_URL'), config.get('OPTIM_USERNAME'), config.get('OPTIM_PASSWORD')]):
        print("❌ Missing Optim configuration in .env file")
        return 1
    
    try:
        # Authenticate
        print("🔐 Authenticating with Optim API...")
        auth = OptimAuthHelper(
            config['OPTIM_BASE_URL'],
            config['OPTIM_USERNAME'],
            config['OPTIM_PASSWORD']
        )
        
        # Force fresh authentication
        access_token = auth.get_access_token(force_refresh=True)
        if not access_token:
            print("❌ Authentication failed")
            return 1
        
        print("✅ Authentication successful\n")
        
        # Set up headers
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        if config.get('OPTIM_ACCOUNT_ID'):
            headers['account-id'] = config['OPTIM_ACCOUNT_ID']
        
        base_url = config['OPTIM_BASE_URL'].rstrip('/')
        
        # List all connection profiles
        profiles = list_connection_profiles(base_url, headers)
        
        if not profiles:
            print("❌ No connection profiles found")
            return 1
        
        # Get optional schema and table from config
        schema_name = config.get('OPTIM_SCHEMA_NAME')
        table_name = config.get('OPTIM_TABLE_NAME')
        
        # If specific connection profile is set, use only that one
        if config.get('OPTIM_CONN_PROFILE'):
            target_profile = config['OPTIM_CONN_PROFILE']
            print(f"🎯 Using specific connection profile from config: {target_profile}\n")
            inspect_connection_data(base_url, headers, target_profile, schema_name, table_name)
        else:
            # Inspect data from all connection profiles
            print("🔍 Inspecting data from all connection profiles...\n")
            for profile in profiles:
                profile_name = profile.get('name')
                if profile_name:
                    success = inspect_connection_data(base_url, headers, profile_name, schema_name, table_name)
                    if not success:
                        print(f"⚠️  Skipping connection profile '{profile_name}' due to errors\n")
        
        print("\n" + "="*70)
        print("  INSPECTION COMPLETE")
        print("="*70)
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())

# Made with Bob
