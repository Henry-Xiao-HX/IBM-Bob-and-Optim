# IBM Optim Archive API Toolkit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive, production-ready toolkit for working with IBM Optim Archive API. Features include automated authentication, interactive demos, and a real-time Business Intelligence dashboard for monitoring archival operations.

## ✨ Features

- 🔐 **Automated Authentication** - Token management with 23-hour caching
- 🎯 **Interactive Demo Scripts** - Explore API capabilities step-by-step
- 📊 **BI Dashboard** - Real-time monitoring and analytics
- 🎲 **Test Data Management** - Synthetic test data generation for DevOps CI/CD
- 🔧 **Reusable Components** - Import as library or use standalone
- 📚 **Comprehensive Documentation** - API reference and setup guides
- 🚀 **Production Ready** - Error handling, logging, and best practices

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

## 🌐 Web UI Access

Access the Optim Archive Web Interface:

**URL:** https://host:7780/

**Credentials:**
```env
OPTIM_USERNAME=your_username
OPTIM_PASSWORD=your_password
```

> **Note:** Replace `host` with your actual Optim server hostname or IP address. Use your configured Optim credentials to log in.

## 📊 Business Intelligence Dashboard

Monitor and analyze your archival operations with real-time insights:

```bash
cd dashboard
./launch_dashboard.sh
```

Then open: **http://localhost:5001**

### Dashboard Features
- 📈 **Summary Metrics**: Jobs, executions, archives, success rates
- 👥 **Business Unit Analytics**: Track who's archiving what
- 📊 **Interactive Charts**: Visualize trends and distributions
- 🔄 **Auto-refresh**: Real-time updates every 5 minutes

For detailed dashboard documentation, see the dashboard section below.

## 🎲 Test Data Management (TDM)

**NEW: Synthetic Test Data Generation for DevOps Teams**

Generate privacy-compliant, production-like test data directly in your IDE using IBM BOB and Optim Archive APIs.

```bash
cd TDM
python3 synthetic_testdata_demo.py
```

### Key Benefits

- **🔍 Data Discovery** - Find production data structures without accessing sensitive data
- **✂️ Data Subsetting** - Extract manageable samples for test environments
- **🔒 Privacy Masking** - Automatic PII/PHI masking for compliance (GDPR, HIPAA)
- **🎲 Synthetic Generation** - Create realistic test data with production patterns
- **🧪 Pre-Commit Testing** - Validate code changes before committing
- **🚀 CI/CD Ready** - Export to JSON, SQL, CSV for pipeline integration

### Quick Demo

```bash
# Generate synthetic test data
cd TDM
python3 synthetic_testdata_demo.py

# Test your application with synthetic data
cd mock_app
python3 app.py

# Run pre-commit tests
python3 test_app.py
```

### Use with IBM BOB

IBM BOB can guide you through the entire workflow interactively:

1. **Ask BOB**: "Help me test my code changes with synthetic data"
2. **BOB will**:
   - Check if you have test data (or generate it)
   - Run your application with test data
   - Execute automated tests
   - Tell you if it's safe to commit

See [`TDM/README.md`](TDM/README.md) for complete documentation.

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
├── TDM/                          # Test Data Management
│   ├── README.md                 # TDM documentation
│   ├── synthetic_testdata_demo.py # Synthetic data generator
│   └── mock_app/                 # Example application with tests
│       ├── app.py                # Sample credit risk app
│       ├── test_app.py           # Pre-commit test suite
│       └── credit_risk_mock_data.csv # Sample test data
│
├── docs/
│   └── API_REFERENCE.md          # Complete API endpoint reference
│
├── examples/                     # Usage examples
│   ├── basic_authentication.py   # Authentication example
│   └── list_archive_jobs.py      # List jobs example
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

## 📚 Documentation & Examples

| Resource | Description |
|----------|-------------|
| **[API Reference](docs/API_REFERENCE.md)** | Complete API endpoint documentation |
| **[Code Examples](examples/)** | Practical usage examples |
| **[Dashboard Guide](#-business-intelligence-dashboard)** | BI dashboard documentation (see above) |

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

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for IBM Optim Archive API
- Designed for enterprise archival management
- Community contributions welcome

## 📞 Support

For issues, questions, or contributions:
- 📝 [Open an issue](../../issues)
- 💬 [Start a discussion](../../discussions)
- 🔀 [Submit a pull request](../../pulls)

---

**Built for easy demos and efficient archival management** 🎯