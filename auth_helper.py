#!/usr/bin/env python3
"""
IBM Optim Archive API Authentication Helper
Handles token retrieval and caching for easy demos
"""

import requests
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict
import urllib3

# Disable SSL warnings for demo environments
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class OptimAuthHelper:
    """Helper class to manage Optim API authentication"""
    
    TOKEN_CACHE_FILE = ".token_cache.json"
    
    def __init__(self, base_url: str, username: str, password: str):
        """
        Initialize auth helper
        
        Args:
            base_url: Optim API base URL (e.g., https://VM_HOSTNAME:7725/optim)
            username: Optim username
            password: Optim password
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.token_cache_path = Path(self.TOKEN_CACHE_FILE)
    
    def get_access_token(self, force_refresh: bool = False) -> Optional[str]:
        """
        Get a valid access token (from cache or by authenticating)
        
        Args:
            force_refresh: Force token refresh even if cached token exists
            
        Returns:
            Access token string or None if authentication fails
        """
        # Try to use cached token first
        if not force_refresh:
            cached_token = self._get_cached_token()
            if cached_token:
                print("✅ Using cached access token")
                return cached_token
        
        # Fetch new token
        print("🔄 Fetching new access token...")
        token = self._fetch_new_token()
        
        if token:
            self._cache_token(token)
            print("✅ Access token retrieved and cached")
        else:
            print("❌ Failed to retrieve access token")
        
        return token
    
    def _fetch_new_token(self) -> Optional[str]:
        """Fetch a new access token from the API"""
        url = f"{self.base_url}/v1/auth/token"
        
        data = {
            'username': self.username,
            'password': self.password
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            response = requests.post(
                url,
                data=data,
                headers=headers,
                verify=False,  # Disable SSL verification for demo
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                token = result.get('requestObj', {}).get('access_token')
                return token
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON response: {e}")
            return None
    
    def _get_cached_token(self) -> Optional[str]:
        """Get token from cache if valid"""
        if not self.token_cache_path.exists():
            return None
        
        try:
            with open(self.token_cache_path, 'r') as f:
                cache = json.load(f)
            
            # Check if token is expired (assuming 24 hour validity)
            cached_time = datetime.fromisoformat(cache.get('timestamp', ''))
            expiry_time = cached_time + timedelta(hours=23)  # Refresh 1 hour before expiry
            
            if datetime.now() < expiry_time:
                return cache.get('token')
            else:
                print("⚠️  Cached token expired")
                return None
                
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"⚠️  Invalid token cache: {e}")
            return None
    
    def _cache_token(self, token: str):
        """Cache the token with timestamp"""
        cache = {
            'token': token,
            'timestamp': datetime.now().isoformat(),
            'username': self.username,
            'base_url': self.base_url
        }
        
        with open(self.token_cache_path, 'w') as f:
            json.dump(cache, f, indent=2)
    
    def clear_cache(self):
        """Clear the token cache"""
        if self.token_cache_path.exists():
            self.token_cache_path.unlink()
            print("✅ Token cache cleared")


def load_config_from_env() -> Dict[str, str]:
    """
    Load configuration from .env file
    
    Returns:
        Dictionary with configuration values
    """
    config = {}
    env_path = Path('.env')
    
    if not env_path.exists():
        return config
    
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    
    return config


def get_token_interactive() -> Optional[str]:
    """
    Interactive token retrieval - prompts user for credentials
    
    Returns:
        Access token or None
    """
    print("\n" + "="*60)
    print("  IBM OPTIM API - TOKEN RETRIEVAL")
    print("="*60 + "\n")
    
    # Try to load from .env first
    config = load_config_from_env()
    
    if config.get('OPTIM_BASE_URL') and config.get('OPTIM_USERNAME') and config.get('OPTIM_PASSWORD'):
        print("📋 Found credentials in .env file")
        use_env = input("Use these credentials? (Y/n): ").strip().lower()
        
        if use_env != 'n':
            base_url = config['OPTIM_BASE_URL']
            username = config['OPTIM_USERNAME']
            password = config['OPTIM_PASSWORD']
        else:
            base_url = input("API Base URL: ").strip()
            username = input("Username: ").strip()
            password = input("Password: ").strip()
    else:
        print("Please provide your credentials:\n")
        base_url = input("API Base URL (e.g., https://VM_HOSTNAME:7725/optim): ").strip()
        username = input("Username: ").strip()
        password = input("Password: ").strip()
    
    if not all([base_url, username, password]):
        print("\n❌ All fields are required!")
        return None
    
    print()
    auth = OptimAuthHelper(base_url, username, password)
    return auth.get_access_token()


def main():
    """Main entry point for standalone token retrieval"""
    token = get_token_interactive()
    
    if token:
        print("\n" + "="*60)
        print("✅ SUCCESS!")
        print("="*60)
        print(f"\nYour access token:\n{token}\n")
        print("💡 Token has been cached for future use")
        print("💡 Use this token in your API calls or demo scripts")
        print()
    else:
        print("\n❌ Failed to retrieve token")


if __name__ == "__main__":
    main()
