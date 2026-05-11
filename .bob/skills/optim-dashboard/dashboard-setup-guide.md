# Dashboard Setup Guide

## Prerequisites

- Python 3.7+
- IBM Optim Archive API access
- Valid credentials configured in `.env` file

## Quick Start

```bash
# Navigate to dashboard directory
cd dashboard

# Install dependencies
pip install -r requirements.txt

# Launch dashboard
./launch_dashboard.sh
```

Access at: http://localhost:5001

## Configuration

The dashboard uses the same `.env` file as the main project:

```env
OPTIM_BASE_URL=https://your-optim-server:7725/optim
OPTIM_USERNAME=your_username
OPTIM_PASSWORD=your_password
OPTIM_ACCOUNT_ID=your_account_id  # Optional
```

## Architecture

```
dashboard/
├── dashboard_server.py      # Flask web server
├── bi_data_collector.py     # Data collection from API
├── templates/
│   └── dashboard.html       # Frontend UI
└── requirements.txt         # Python dependencies
```

### Components

1. **Flask Server** (`dashboard_server.py`)
   - Serves the web interface
   - Provides REST API endpoints
   - Handles authentication
   - Implements caching (5-minute default)

2. **Data Collector** (`bi_data_collector.py`)
   - Fetches data from Optim API
   - Processes and aggregates metrics
   - Handles errors gracefully

3. **Frontend** (`dashboard.html`)
   - Responsive card-based layout
   - Chart.js visualizations
   - Auto-refresh every 5 minutes
   - Real-time metric updates

## Available Endpoints

| Endpoint | Description |
|----------|-------------|
| `/` | Main dashboard page |
| `/api/metrics` | All metrics (cached) |
| `/api/summary` | Summary statistics |
| `/api/jobs` | Job metrics |
| `/api/executions` | Execution metrics |
| `/api/archives` | Archive metrics |
| `/api/business-units` | Business unit breakdown |

## Customization

### Change Port

Edit `dashboard_server.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Adjust Cache Duration

Edit `dashboard_server.py`:
```python
CACHE_DURATION_SECONDS = 300  # 5 minutes
```

### Modify Auto-Refresh

Edit `dashboard.html`:
```javascript
setInterval(loadAllData, 300000); // 5 minutes in milliseconds
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 5001
lsof -i :5001

# Kill the process
kill -9 <PID>
```

### Authentication Errors
- Verify `.env` file exists in project root
- Check credentials are correct
- Ensure API is accessible from your network

### No Data Displayed
- Check browser console for errors
- Verify API endpoints return data
- Check cache hasn't expired
- Force refresh with `?refresh=true` parameter