#!/usr/bin/env python3
"""
Example: Basic Authentication with IBM Optim Archive API

This example demonstrates how to authenticate and get an access token
using the auth_helper module.
"""

import sys
from pathlib import Path

# Add parent directory to path to import auth_helper
sys.path.insert(0, str(Path(__file__).parent.parent))

from auth_helper import OptimAuthHelper, load_config_from_env


def main():
    """Demonstrate basic authentication"""
    print("=" * 60)
    print("Example: Basic Authentication")
    print("=" * 60)
    
    # Load configuration from .env file
    config = load_config_from_env()
    
    if not all([config.get('OPTIM_BASE_URL'), 
                config.get('OPTIM_USERNAME'), 
                config.get('OPTIM_PASSWORD')]):
        print("\n❌ Error: Missing required configuration in .env file")
        print("   Please ensure OPTIM_BASE_URL, OPTIM_USERNAME, and OPTIM_PASSWORD are set")
        return
    
    # Initialize auth helper
    auth = OptimAuthHelper(
        base_url=config['OPTIM_BASE_URL'],
        username=config['OPTIM_USERNAME'],
        password=config['OPTIM_PASSWORD']
    )
    
    # Get access token (will use cache if available)
    print("\nAttempting to get access token...")
    token = auth.get_access_token()
    
    if token:
        print(f"\n✅ Successfully authenticated!")
        print(f"   Token: {token[:20]}...{token[-20:]}")
        print(f"\n💡 Token is cached and will be reused for 23 hours")
    else:
        print("\n❌ Authentication failed")
        return
    
    # Force refresh example
    print("\n" + "-" * 60)
    print("Example: Force token refresh")
    print("-" * 60)
    
    new_token = auth.get_access_token(force_refresh=True)
    if new_token:
        print("✅ Token refreshed successfully")


if __name__ == "__main__":
    main()
