# IBM Optim Archive API - Demo & Tools

A comprehensive toolkit for working with IBM Optim Archive API, featuring demo scripts, authentication helpers, and a Business Intelligence dashboard for monitoring archival operations.

## 🚀 Quick Start

### 1. Setup Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

Required configuration:
```env
OPTIM_BASE_URL=https://your-optim-server:7725/optim
OPTIM_USERNAME=your_username
OPTIM_PASSWORD=your_password
```

### 2. Run the Demo

```bash
# Option 1: Use the quick launcher (recommended)
./quick_demo.sh

# Option 2: Run directly
python3 demo_optim_api.py
```

The demo will automatically:
- ✅ Authenticate with the API
- ✅ Cache tokens for 23 hours
- ✅ Showcase all key API capabilities
- ✅ Provide interactive walkthroughs

## 📊 Business Intelligence Dashboard

Monitor and analyze your archival operations with real-time insights:

```bash
cd dashboard
./launch_dashboard.sh
```

Then open: **http://localhost:5000**

### Dashboard Features
- 📈 **Summary Metrics**: Jobs, executions, archives, success rates
- 👥 **Business Unit Analytics**: Track who's archiving what
- 📊 **Interactive Charts**: Visualize trends and distributions
- 🔄 **Auto-refresh**: Real-time updates every 5 minutes

**[📖 Dashboard Quick Start](docs/DASHBOARD_QUICKSTART.md)** | **[📚 Full Dashboard Docs](dashboard/README.md)**

## 📁 Project Structure

```
.
├── README.md                      # This file
├── .env.example                   # Configuration template
├── .gitignore                     # Git ignore rules
│
├── demo_optim_api.py             # Interactive API demo script
├── auth_helper.py                # Authentication & token management
├── quick_demo.sh                 # One-command demo launcher
│
├── docs/                         # Documentation
│   ├── API_Analysis.md           # API endpoint reference
│   ├── DEMO_SETUP.md             # Detailed setup guide
│   └── DASHBOARD_QUICKSTART.md   # Dashboard quick start
│
└── dashboard/                    # BI Dashboard
    ├── dashboard_server.py       # Flask web server
    ├── bi_data_collector.py      # Data collection module
    ├── launch_dashboard.sh       # Dashboard launcher
    ├── requirements.txt          # Python dependencies
    ├── README.md                 # Dashboard documentation
    └── templates/
        └── dashboard.html        # Dashboard UI
```

## 🔑 Authentication

The toolkit provides automatic authentication with token caching:

### Automatic (Recommended)
```bash
# Credentials from .env file
python3 demo_optim_api.py
```

### Manual Token Retrieval
```bash
# Get and cache a token
python3 auth_helper.py
```

### Token Features
- ✅ Automatic retrieval from API
- ✅ Cached for 23 hours
- ✅ Auto-refresh when expired
- ✅ Secure storage in `.token_cache.json`

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[API Analysis](docs/API_Analysis.md)** | Complete API endpoint reference |
| **[Demo Setup Guide](docs/DEMO_SETUP.md)** | Detailed setup instructions |
| **[Dashboard Quick Start](docs/DASHBOARD_QUICKSTART.md)** | Get started with the BI dashboard |
| **[Dashboard README](dashboard/README.md)** | Full dashboard documentation |

## 🎯 Key Features

### Demo Script (`demo_optim_api.py`)
- Interactive walkthrough of API capabilities
- Automatic authentication
- Step-by-step demonstrations:
  - List archive jobs
  - View job details and execution history
  - Browse archive schemas and tables
  - Sample archived data

### Authentication Helper (`auth_helper.py`)
- Automatic token retrieval
- Token caching (23-hour expiration)
- Support for `.env` configuration
- Standalone or library usage

### BI Dashboard
- Real-time metrics and analytics
- Business unit performance tracking
- Interactive visualizations
- RESTful API endpoints

## 🛠️ Requirements

- Python 3.7+
- Required packages:
  ```bash
  pip install requests urllib3 flask
  ```

## 🔒 Security Notes

- ✅ `.env` and `.token_cache.json` are gitignored
- ✅ SSL verification disabled for demo environments
- ⚠️ Never commit credentials to version control
- ⚠️ Keep `.env` file secure

## 💡 Usage Examples

### Run Interactive Demo
```bash
./quick_demo.sh
```

### Get Access Token
```bash
python3 auth_helper.py
```

### Launch Dashboard
```bash
cd dashboard && ./launch_dashboard.sh
```

### Use as Library
```python
from auth_helper import OptimAuthHelper, load_config_from_env

config = load_config_from_env()
auth = OptimAuthHelper(
    config['OPTIM_BASE_URL'],
    config['OPTIM_USERNAME'],
    config['OPTIM_PASSWORD']
)
token = auth.get_access_token()
```

## 🤝 Contributing

This is a demo/tool repository. Feel free to:
- Report issues
- Suggest improvements
- Submit pull requests

## 📄 License

This project is provided as-is for demonstration and utility purposes.

---

**Built for easy demos and efficient archival management** 🎯