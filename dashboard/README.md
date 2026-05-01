# IBM Optim Archive - Business Intelligence Dashboard

A comprehensive web-based dashboard for monitoring and analyzing IBM Optim Archive activities, providing insights into archival jobs, executions, and business unit performance.

## 🎯 Features

### Key Metrics Tracked
- **Total Archive Jobs**: Number of configured archival jobs
- **Total Executions**: Number of job runs across all jobs
- **Archive Files**: Total archived data files created
- **Business Units**: Unique users/departments using the system
- **Success Rate**: Overall job execution success percentage
- **Average Duration**: Mean execution time for archival jobs

### Visualizations
1. **Jobs by Business Unit** - Bar chart showing job distribution
2. **Job Status Distribution** - Doughnut chart of job statuses
3. **Executions by Business Unit** - Bar chart of execution counts
4. **Archives by Business Unit** - Bar chart of archive file counts
5. **Business Unit Details Table** - Comprehensive breakdown with success rates

### Business Intelligence Insights
- **Who committed**: Track which business units/users are creating archives
- **What was committed**: View job details, schemas, and tables archived
- **How much committed**: Monitor execution counts, archive files, and data volumes
- **Performance metrics**: Success rates and execution durations per business unit

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Access to IBM Optim Archive API
- `.env` file configured in parent directory

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or install individually
pip install flask requests urllib3
```

### Configuration

Ensure your `.env` file in the parent directory contains:

```env
OPTIM_BASE_URL=https://your-optim-server:7725/optim
OPTIM_USERNAME=your_username
OPTIM_PASSWORD=your_password
OPTIM_ACCOUNT_ID=your_account_id  # Optional
```

### Running the Dashboard

#### Option 1: Using the launcher script
```bash
cd dashboard
./launch_dashboard.sh
```

#### Option 2: Direct Python execution
```bash
cd dashboard
python3 dashboard_server.py
```

#### Option 3: From parent directory
```bash
python3 -m dashboard.dashboard_server
```

### Accessing the Dashboard

Once started, open your browser and navigate to:
```
http://localhost:5000
```

The dashboard will automatically:
- Authenticate with the Optim API
- Collect metrics from all endpoints
- Display real-time visualizations
- Auto-refresh every 5 minutes

## 📊 Dashboard Components

### Summary Cards
Six key metric cards at the top provide at-a-glance statistics:
- Total jobs, executions, and archives
- Unique business units
- Overall success rate
- Average execution duration

### Interactive Charts
Four dynamic charts powered by Chart.js:
- **Bar Charts**: Compare metrics across business units
- **Doughnut Chart**: Visualize job status distribution
- Color-coded for easy interpretation

### Business Unit Table
Detailed breakdown showing:
- Business unit/user name
- Number of jobs created
- Total executions
- Archive files generated
- Success rate (color-coded: green ≥80%, yellow ≥50%, red <50%)

## 🔄 Data Collection

The dashboard uses `bi_data_collector.py` to gather data from multiple API endpoints:

1. **Job Metrics** (`/v1/job/savedlist`)
   - All archive jobs
   - Job creators and owners
   - Job statuses

2. **Execution Metrics** (`/v1/job/spark/status/{id}`)
   - Execution history
   - Success/failure rates
   - Duration statistics

3. **Archive Metrics** (`/v1/file/savedlist`)
   - Archive files created
   - File metadata
   - Creation timestamps

### Caching
- Metrics are cached for 5 minutes to reduce API load
- Manual refresh available via dashboard button
- Automatic refresh every 5 minutes

## 🛠️ Standalone Data Collection

You can also run the data collector independently:

```bash
cd dashboard
python3 bi_data_collector.py
```

This will:
- Collect all metrics
- Save to `bi_metrics.json`
- Display summary statistics

## 📁 Project Structure

```
dashboard/
├── bi_data_collector.py      # Data collection module
├── dashboard_server.py        # Flask web server
├── templates/
│   └── dashboard.html         # Dashboard UI
├── requirements.txt           # Python dependencies
├── launch_dashboard.sh        # Launcher script
└── README.md                  # This file
```

## 🔧 API Endpoints

The dashboard server exposes several REST endpoints:

- `GET /` - Main dashboard page
- `GET /api/metrics` - All metrics (with optional `?refresh=true`)
- `GET /api/summary` - Summary statistics only
- `GET /api/jobs` - Job metrics
- `GET /api/executions` - Execution metrics
- `GET /api/archives` - Archive metrics
- `GET /api/business-units` - Business unit breakdown

## 🎨 Customization

### Modify Refresh Interval
Edit `dashboard_server.py`:
```python
CACHE_DURATION_SECONDS = 300  # Change to desired seconds
```

Edit `dashboard.html`:
```javascript
setInterval(loadDashboard, 300000);  // Change to desired milliseconds
```

### Add Custom Metrics
1. Add collection logic to `bi_data_collector.py`
2. Create new API endpoint in `dashboard_server.py`
3. Add visualization to `dashboard.html`

## 🐛 Troubleshooting

### Dashboard won't start
- Check `.env` file exists in parent directory
- Verify Python dependencies are installed
- Ensure port 5000 is not in use

### No data displayed
- Verify Optim API credentials are correct
- Check network connectivity to Optim server
- Review browser console for JavaScript errors
- Check terminal for Python errors

### Authentication failures
- Confirm username/password in `.env`
- Verify API base URL is correct
- Check if token cache is stale (delete `.token_cache.json`)

## 📈 Performance Considerations

- Dashboard caches data for 5 minutes by default
- Execution history limited to 5 runs per job (first 10 jobs)
- Adjust limits in `bi_data_collector.py` for larger datasets
- Consider implementing pagination for large result sets

## 🔒 Security Notes

- Dashboard runs on localhost by default
- SSL verification disabled for demo environments
- Do not expose dashboard to public internet without authentication
- Keep `.env` file secure and never commit to version control

## 📝 Future Enhancements

Potential improvements:
- [ ] User authentication for dashboard access
- [ ] Export metrics to CSV/Excel
- [ ] Historical trend analysis
- [ ] Email alerts for failed jobs
- [ ] Custom date range filtering
- [ ] Drill-down into specific jobs
- [ ] Real-time execution monitoring
- [ ] Data volume tracking (GB archived)

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation in `../API_Analysis.md`
3. Verify Optim API connectivity

---

**Made with Bob** 🎯