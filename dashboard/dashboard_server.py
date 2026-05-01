#!/usr/bin/env python3
"""
Business Intelligence Dashboard Server for IBM Optim Archive
Flask-based web server with real-time data visualization
"""

from flask import Flask, render_template, jsonify, request
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path to import auth_helper
sys.path.insert(0, str(Path(__file__).parent.parent))

from auth_helper import OptimAuthHelper, load_config_from_env

# Import collector from current directory
if __name__ == "__main__":
    from bi_data_collector import ArchivalBICollector
else:
    from dashboard.bi_data_collector import ArchivalBICollector

app = Flask(__name__)

# Global variables for caching
cached_metrics = None
last_update = None
CACHE_DURATION_SECONDS = 300  # 5 minutes


def get_metrics(force_refresh=False):
    """Get metrics with caching"""
    global cached_metrics, last_update
    
    # Check if cache is valid
    if not force_refresh and cached_metrics and last_update:
        elapsed = (datetime.now() - last_update).total_seconds()
        if elapsed < CACHE_DURATION_SECONDS:
            return cached_metrics
    
    # Change to parent directory to find .env file
    import os
    original_dir = os.getcwd()
    parent_dir = Path(__file__).parent.parent
    os.chdir(parent_dir)
    
    # Load configuration
    config = load_config_from_env()
    
    # Change back to original directory
    os.chdir(original_dir)
    
    if not config.get('OPTIM_BASE_URL'):
        return {'error': 'Configuration not found'}
    
    base_url = config['OPTIM_BASE_URL']
    username = config['OPTIM_USERNAME']
    password = config['OPTIM_PASSWORD']
    account_id = config.get('OPTIM_ACCOUNT_ID', '')
    
    # Get access token
    auth = OptimAuthHelper(base_url, username, password)
    access_token = auth.get_access_token()
    
    if not access_token:
        return {'error': 'Failed to authenticate'}
    
    # Collect metrics
    collector = ArchivalBICollector(
        base_url=base_url,
        access_token=access_token,
        account_id=account_id if account_id else None
    )
    
    metrics = collector.collect_all_metrics()
    
    # Update cache
    cached_metrics = metrics
    last_update = datetime.now()
    
    return metrics


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/metrics')
def api_metrics():
    """API endpoint to get all metrics"""
    force_refresh = request.args.get('refresh', 'false').lower() == 'true'
    metrics = get_metrics(force_refresh=force_refresh)
    return jsonify(metrics)


@app.route('/api/summary')
def api_summary():
    """API endpoint to get summary statistics"""
    metrics = get_metrics()
    return jsonify(metrics.get('summary', {}))


@app.route('/api/jobs')
def api_jobs():
    """API endpoint to get job metrics"""
    metrics = get_metrics()
    return jsonify(metrics.get('jobs', {}))


@app.route('/api/executions')
def api_executions():
    """API endpoint to get execution metrics"""
    metrics = get_metrics()
    return jsonify(metrics.get('executions', {}))


@app.route('/api/archives')
def api_archives():
    """API endpoint to get archive metrics"""
    metrics = get_metrics()
    return jsonify(metrics.get('archives', {}))


@app.route('/api/business-units')
def api_business_units():
    """API endpoint to get business unit breakdown"""
    metrics = get_metrics()
    jobs = metrics.get('jobs', {})
    executions = metrics.get('executions', {})
    archives = metrics.get('archives', {})
    
    # Combine data by user/business unit
    business_units = {}
    
    # From jobs
    for user, user_jobs in jobs.get('by_user', {}).items():
        if user not in business_units:
            business_units[user] = {
                'business_unit_id': 1,
                'name': user,
                'jobs': 0,
                'executions': 0,
                'archives': 0,
                'success_rate': 0
            }
        business_units[user]['jobs'] = len(user_jobs)
    
    # From executions
    for user, exec_data in executions.get('by_user', {}).items():
        if user not in business_units:
            business_units[user] = {
                'business_unit_id': 1,
                'name': user,
                'jobs': 0,
                'executions': 0,
                'archives': 0,
                'success_rate': 0
            }
        business_units[user]['executions'] = exec_data.get('runs', 0)
        total = exec_data.get('runs', 0)
        success = exec_data.get('success', 0)
        if total > 0:
            business_units[user]['success_rate'] = round((success / total) * 100, 2)
    
    # From archives
    for user, user_archives in archives.get('by_user', {}).items():
        if user not in business_units:
            business_units[user] = {
                'business_unit_id': 1,
                'name': user,
                'jobs': 0,
                'executions': 0,
                'archives': 0,
                'success_rate': 0
            }
        business_units[user]['archives'] = len(user_archives)
    
    return jsonify(list(business_units.values()))


def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("  IBM OPTIM ARCHIVE - BI DASHBOARD SERVER")
    print("="*60 + "\n")
    
    # Store the script's directory for Flask reloader
    import os
    script_dir = Path(__file__).parent
    parent_dir = script_dir.parent
    
    # Set environment variable for Flask reloader to find the script
    os.environ['FLASK_APP'] = str(Path(__file__).absolute())
    
    # Change to parent directory to find .env file
    os.chdir(parent_dir)
    
    # Check for configuration
    config = load_config_from_env()
    if not config.get('OPTIM_BASE_URL'):
        print("❌ Error: .env file not found or incomplete")
        print("Please create a .env file in the project root with your credentials")
        return
    
    print("✅ Configuration loaded")
    print("\n🚀 Starting dashboard server...")
    print("\n📊 Dashboard URL: http://localhost:5001")
    print("\n💡 Press Ctrl+C to stop the server\n")
    
    # Run Flask app with reloader disabled to avoid path issues
    # Users can manually restart if they make changes
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)


if __name__ == "__main__":
    main()

# Made with Bob