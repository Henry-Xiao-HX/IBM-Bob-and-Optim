# IBM Optim Archive API - Demo Setup Guide

This guide will help you set up and run demos quickly without worrying about authentication.

## 🚀 Quick Start (Recommended)

### 1. One-Time Setup

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```bash
# IBM Optim Archive API Configuration
OPTIM_BASE_URL=https://your-vm-hostname:7725/optim
OPTIM_USERNAME=your_username
OPTIM_PASSWORD=your_password
OPTIM_ACCOUNT_ID=
```

### 2. Run the Demo

Simply run the demo script - it will automatically handle authentication:

```bash
python3 demo_optim_api.py
```

**That's it!** The script will:
- ✅ Automatically retrieve your access token
- ✅ Cache the token for 23 hours (no repeated logins)
- ✅ Auto-refresh when the token expires
- ✅ Run the full interactive demo

## 🔧 Alternative Methods

### Method 1: Standalone Token Retrieval

If you just need to get a token for manual testing:

```bash
python3 auth_helper.py
```

This will:
1. Prompt for credentials (or use `.env` if available)
2. Retrieve and display your access token
3. Cache it for future use

### Method 2: Manual Token Retrieval (Original Method)

Use curl to get a token manually:

```bash
curl -kX POST https://VM_HOSTNAME:7725/optim/v1/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'username={user}&password={password}' | jq '.requestObj.access_token'
```

Then add it to your `.env` file:

```bash
OPTIM_ACCESS_TOKEN=your_token_here
```

### Method 3: Interactive Mode (No .env file)

Run the demo without a `.env` file - it will prompt for credentials:

```bash
python3 demo_optim_api.py
```

The script will ask for:
- API Base URL
- Username
- Password
- Account ID (optional)

## 📁 Files Overview

| File | Purpose |
|------|---------|
| `demo_optim_api.py` | Main demo script with auto-authentication |
| `auth_helper.py` | Authentication helper with token caching |
| `.env` | Your credentials (create from `.env.example`) |
| `.env.example` | Template for credentials file |
| `.token_cache.json` | Cached token (auto-generated, expires in 24h) |

## 🔒 Security Notes

- ✅ `.env` and `.token_cache.json` are in `.gitignore` (won't be committed)
- ✅ Token cache expires after 23 hours
- ✅ SSL verification disabled for demo environments (can be enabled in production)
- ⚠️ Never commit `.env` or share your credentials

## 💡 Tips for Demos

### Before Your Demo

1. **Test your connection:**
   ```bash
   python3 auth_helper.py
   ```
   This ensures your credentials work and caches the token.

2. **Verify the demo runs:**
   ```bash
   python3 demo_optim_api.py
   ```

### During Your Demo

- The script handles all authentication automatically
- Token is cached, so no delays during the demo
- Interactive prompts let you control the pace
- Clear, formatted output perfect for presentations

### After Your Demo

- Token remains cached for other demos
- No cleanup needed
- Run `python3 auth_helper.py` to refresh if needed

## 🛠️ Troubleshooting

### "Failed to retrieve access token"

1. Check your credentials in `.env`
2. Verify the VM hostname is correct
3. Ensure the Optim service is running
4. Check network connectivity to the VM

### "Cached token expired"

The script will automatically fetch a new token. If this fails:

```bash
# Clear the cache and try again
rm .token_cache.json
python3 auth_helper.py
```

### SSL Certificate Errors

The scripts disable SSL verification for demo environments. If you need to enable it:

1. Edit `auth_helper.py` and `demo_optim_api.py`
2. Change `verify=False` to `verify=True`
3. Ensure proper SSL certificates are configured

## 📝 Example Workflow

```bash
# First time setup
cp .env.example .env
nano .env  # Add your credentials

# Get and cache token
python3 auth_helper.py

# Run demo (uses cached token)
python3 demo_optim_api.py

# Run demo again later (still uses cached token)
python3 demo_optim_api.py

# Token auto-refreshes after 23 hours
```

## 🎯 What the Demo Shows

The demo script showcases:

1. **Job Listing** - List all archive jobs with filtering
2. **Job Details** - Get detailed job configuration
3. **Execution History** - View job run history and status
4. **Schema Browsing** - Explore archived database schemas
5. **Table Metadata** - Get table structure and column info
6. **Data Sampling** - Preview archived data

All via REST API calls with JSON responses!

## 🔄 Token Lifecycle

```
┌─────────────────────────────────────────────────────┐
│ 1. First Run                                        │
│    - Reads credentials from .env                    │
│    - Calls /v1/auth/token API                       │
│    - Caches token in .token_cache.json              │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 2. Subsequent Runs (within 23 hours)                │
│    - Reads token from .token_cache.json             │
│    - No API call needed                             │
│    - Instant demo start                             │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 3. After 23 Hours                                   │
│    - Detects expired token                          │
│    - Auto-fetches new token                         │
│    - Updates cache                                  │
└─────────────────────────────────────────────────────┘
```

---

**Made with ❤️ for easy demos**