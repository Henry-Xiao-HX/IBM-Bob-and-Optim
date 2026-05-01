# 📊 Business Intelligence Dashboard - Quick Start Guide

## Overview

The BI Dashboard provides comprehensive insights into your IBM Optim Archive operations, answering key questions:

- **How much have I committed?** - Total jobs, executions, and archive files
- **What have I committed?** - Detailed job information, schemas, and tables
- **Who's committing?** - Business unit breakdown with performance metrics

## 🚀 Quick Start (3 Steps)

### Step 1: Ensure Configuration
Make sure your `.env` file exists in the project root with:
```env
OPTIM_BASE_URL=https://your-optim-server:7725/optim
OPTIM_USERNAME=your_username
OPTIM_PASSWORD=your_password
```

### Step 2: Launch Dashboard
```bash
cd dashboard
./launch_dashboard.sh
```

### Step 3: Open Browser
Navigate to: **http://localhost:5000**

That's it! The dashboard will automatically:
- ✅ Authenticate with Optim API
- ✅ Collect all metrics
- ✅ Display real-time visualizations
- ✅ Auto-refresh every 5 minutes

## 📊 What You'll See

### Summary Cards (Top Section)
- **Total Archive Jobs**: All configured archival jobs
- **Total Executions**: Number of times jobs have run
- **Archive Files**: Total archived data files created
- **Business Units**: Unique users/departments
- **Success Rate**: Overall job success percentage
- **Average Duration**: Mean execution time

### Interactive Charts
1. **Jobs by Business Unit** - Who created what jobs
2. **Job Status Distribution** - Success/failure breakdown
3. **Executions by Business Unit** - Who's running jobs
4. **Archives by Business Unit** - Who's creating archives

### Business Unit Table
Detailed breakdown showing:
- Business unit/user name
- Number of jobs created
- Total executions
- Archive files generated
- Success rate (color-coded)

## 🎯 Key Features

### Real-Time Data
- Metrics collected from live Optim API
- Cached for 5 minutes to reduce load
- Manual refresh button available
- Auto-refresh every 5 minutes

### Business Intelligence Insights
- **Commit Volume**: See total jobs, executions, and archives
- **Commit Details**: Drill down into what was archived
- **Business Unit Performance**: Compare success rates across teams
- **Trend Analysis**: Monitor execution patterns

### User-Friendly Interface
- Clean, modern design
- Color-coded metrics (green = good, yellow = warning, red = alert)
- Responsive layout works on all devices
- Interactive charts with Chart.js

## 🔧 Alternative Launch Methods

### Method 1: Direct Python
```bash
cd dashboard
python3 dashboard_server.py
```

### Method 2: From Project Root
```bash
python3 -m dashboard.dashboard_server
```

### Method 3: Standalone Data Collection
```bash
cd dashboard
python3 bi_data_collector.py
# Saves metrics to bi_metrics.json
```

## 📈 Understanding the Metrics

### Jobs
- **Total Jobs**: All archive jobs configured in the system
- **By User**: Shows which business unit/user created each job
- **By Status**: Current status of jobs (FINISHED, FAILED, etc.)
- **By Connection**: Groups jobs by source database connection

### Executions
- **Total Runs**: Number of times jobs have been executed
- **Success Rate**: Percentage of successful executions
- **Failed Runs**: Number of failed executions
- **Duration**: Average time to complete jobs

### Archives
- **Total Archives**: Number of archive files created
- **By User**: Shows which business unit created archives
- **Creation Time**: When archives were created

## 🎨 Dashboard Customization

### Change Refresh Interval
Edit `dashboard_server.py`:
```python
CACHE_DURATION_SECONDS = 300  # Change to desired seconds
```

### Modify Auto-Refresh
Edit `templates/dashboard.html`:
```javascript
setInterval(loadDashboard, 300000);  // Change milliseconds
```

### Add Custom Metrics
1. Add collection logic to `bi_data_collector.py`
2. Create API endpoint in `dashboard_server.py`
3. Add visualization to `templates/dashboard.html`

## 🔍 API Endpoints

The dashboard exposes REST APIs you can use:

- `GET /api/metrics` - All metrics (add `?refresh=true` to force refresh)
- `GET /api/summary` - Summary statistics only
- `GET /api/jobs` - Job metrics
- `GET /api/executions` - Execution metrics
- `GET /api/archives` - Archive metrics
- `GET /api/business-units` - Business unit breakdown

Example:
```bash
curl http://localhost:5000/api/summary
```

## 🐛 Troubleshooting

### Dashboard Won't Start
```bash
# Check .env file exists
ls -la ../.env

# Verify Python dependencies
pip3 list | grep -E "flask|requests"

# Check port availability
lsof -i :5000
```

### No Data Displayed
1. Verify Optim API credentials in `.env`
2. Check network connectivity to Optim server
3. Review browser console (F12) for errors
4. Check terminal output for Python errors

### Authentication Errors
```bash
# Clear token cache
rm ../.token_cache.json

# Test authentication manually
cd ..
python3 auth_helper.py
```

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or change port in dashboard_server.py
app.run(host='0.0.0.0', port=5001, debug=True)
```

## 📊 Sample Use Cases

### 1. Monitor Business Unit Activity
**Question**: Which department is using archival the most?

**Answer**: Check the "Jobs by Business Unit" chart and Business Unit table to see job counts and execution frequency.

### 2. Track Success Rates
**Question**: Are our archival jobs succeeding?

**Answer**: View the "Success Rate" summary card and "Job Status Distribution" chart. Check the Business Unit table for per-team success rates.

### 3. Identify Performance Issues
**Question**: Which jobs are taking too long?

**Answer**: Check "Average Duration" metric. Use the data collector to export detailed execution times for analysis.

### 4. Audit Archival Activity
**Question**: What has been archived and by whom?

**Answer**: Review the Business Unit table for complete breakdown. Use API endpoints to export detailed job and archive information.

## 🔒 Security Notes

- Dashboard runs on localhost by default (not exposed to internet)
- SSL verification disabled for demo environments
- Keep `.env` file secure
- Never commit credentials to version control
- Consider adding authentication for production use

## 📚 Additional Resources

- **Full Documentation**: See `dashboard/README.md`
- **API Documentation**: See `API_Analysis.md`
- **Demo Scripts**: See `demo_optim_api.py`
- **Setup Guide**: See `DEMO_SETUP.md`

## 💡 Tips & Best Practices

1. **Regular Monitoring**: Check dashboard daily to catch issues early
2. **Success Rate Alerts**: If success rate drops below 80%, investigate
3. **Performance Tracking**: Monitor average duration for performance degradation
4. **Business Unit Accountability**: Use metrics to track team usage
5. **Export Data**: Use API endpoints to export metrics for reporting

## 🎯 Next Steps

After launching the dashboard:

1. ✅ Review summary metrics
2. ✅ Identify top business units
3. ✅ Check success rates
4. ✅ Monitor execution patterns
5. ✅ Export data for reporting
6. ✅ Set up regular monitoring schedule

## 🤝 Support

For issues or questions:
1. Check this guide's troubleshooting section
2. Review `dashboard/README.md` for detailed documentation
3. Verify Optim API connectivity
4. Check terminal output for error messages

---

**Ready to get insights?** Run `cd dashboard && ./launch_dashboard.sh` now! 🚀