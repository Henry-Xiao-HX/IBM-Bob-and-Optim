#!/usr/bin/env python3
"""
Business Intelligence Data Collector for IBM Optim Archive
Collects and aggregates archival statistics for dashboard visualization
"""

import requests
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from collections import defaultdict
import urllib3

# Add parent directory to path to import auth_helper
sys.path.insert(0, str(Path(__file__).parent.parent))
from auth_helper import OptimAuthHelper, load_config_from_env

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ArchivalBICollector:
    """Collects business intelligence data from Optim Archive API"""
    
    def __init__(self, base_url: str, access_token: str, account_id: Optional[str] = None):
        """
        Initialize the BI data collector
        
        Args:
            base_url: API base URL
            access_token: API access token
            account_id: Optional account ID for multi-tenant environments
        """
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        if account_id:
            self.headers['account-id'] = account_id
    
    def collect_all_metrics(self) -> Dict:
        """
        Collect all BI metrics in one go
        
        Returns:
            Dictionary containing all metrics
        """
        print("📊 Collecting Business Intelligence Metrics...")
        print("=" * 60)
        
        metrics = {
            'collection_timestamp': datetime.now().isoformat(),
            'jobs': self.get_job_metrics(),
            'executions': self.get_execution_metrics(),
            'archives': self.get_archive_metrics(),
            'summary': {}
        }
        
        # Calculate summary statistics
        metrics['summary'] = self._calculate_summary(metrics)
        
        print("\n✅ Data collection complete!")
        return metrics
    
    def get_job_metrics(self) -> Dict:
        """Get metrics about archive jobs"""
        print("\n📋 Collecting job metrics...")
        
        url = f"{self.base_url}/v1/job/savedlist"
        # Remove worksheet_type filter to get all jobs
        params = {}
        
        try:
            response = requests.get(url, headers=self.headers, params=params, verify=False, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                jobs = result.get('requestObj', {}).get('resources', [])
                
                # Aggregate by business unit (using created_by as proxy)
                by_user = defaultdict(list)
                by_status = defaultdict(int)
                by_connection = defaultdict(list)
                
                for job in jobs:
                    user = job.get('created_by', 'Unknown')
                    status = job.get('last_run_status', 'Unknown')
                    src_conn = job.get('src_conn_name', 'Unknown')
                    
                    by_user[user].append({
                        'id': job.get('id'),
                        'name': job.get('name'),
                        'status': status,
                        'created_at': job.get('created_at'),
                        'last_run': job.get('last_run_time')
                    })
                    
                    by_status[status] += 1
                    by_connection[src_conn].append(job.get('name'))
                
                print(f"   ✓ Found {len(jobs)} jobs")
                print(f"   ✓ {len(by_user)} unique users/business units")
                
                return {
                    'total_jobs': len(jobs),
                    'by_user': dict(by_user),
                    'by_status': dict(by_status),
                    'by_connection': dict(by_connection),
                    'all_jobs': jobs
                }
            else:
                print(f"   ✗ Error: {response.status_code}")
                return {'error': response.text}
                
        except Exception as e:
            print(f"   ✗ Exception: {e}")
            return {'error': str(e)}
    
    def get_execution_metrics(self) -> Dict:
        """Get metrics about job executions"""
        print("\n⚡ Collecting execution metrics...")
        
        # First get all jobs
        url = f"{self.base_url}/v1/job/savedlist"
        # Remove worksheet_type filter to get all jobs
        params = {}
        
        try:
            response = requests.get(url, headers=self.headers, params=params, verify=False, timeout=30)
            
            if response.status_code != 200:
                return {'error': 'Failed to fetch jobs'}
            
            jobs = response.json().get('requestObj', {}).get('resources', [])
            
            all_executions = []
            execution_stats = {
                'total_runs': 0,
                'successful_runs': 0,
                'failed_runs': 0,
                'total_duration_seconds': 0,
                'by_job': {},
                'by_user': defaultdict(lambda: {'runs': 0, 'success': 0, 'failed': 0})
            }
            
            # Get execution history for each job
            for job in jobs[:10]:  # Limit to first 10 jobs for performance
                job_id = job.get('id')
                job_name = job.get('name')
                user = job.get('created_by', 'Unknown')
                
                status_url = f"{self.base_url}/v1/job/spark/status/{job_id}"
                status_params = {'limit': 5}
                
                try:
                    status_response = requests.get(
                        status_url, 
                        headers=self.headers, 
                        params=status_params, 
                        verify=False, 
                        timeout=10
                    )
                    
                    if status_response.status_code == 200:
                        runs = status_response.json()
                        
                        for run in runs:
                            status = run.get('status', 'UNKNOWN')
                            duration = run.get('duration_seconds', 0)
                            
                            all_executions.append({
                                'job_id': job_id,
                                'job_name': job_name,
                                'user': user,
                                'status': status,
                                'start_time': run.get('start_time'),
                                'duration_seconds': duration
                            })
                            
                            execution_stats['total_runs'] += 1
                            execution_stats['total_duration_seconds'] += duration
                            
                            if status == 'FINISHED':
                                execution_stats['successful_runs'] += 1
                                execution_stats['by_user'][user]['success'] += 1
                            elif status == 'FAILED':
                                execution_stats['failed_runs'] += 1
                                execution_stats['by_user'][user]['failed'] += 1
                            
                            execution_stats['by_user'][user]['runs'] += 1
                        
                        execution_stats['by_job'][job_name] = len(runs)
                        
                except Exception as e:
                    print(f"   ⚠ Error fetching status for job {job_id}: {e}")
                    continue
            
            print(f"   ✓ Collected {execution_stats['total_runs']} execution records")
            
            execution_stats['by_user'] = dict(execution_stats['by_user'])
            execution_stats['all_executions'] = all_executions
            
            return execution_stats
            
        except Exception as e:
            print(f"   ✗ Exception: {e}")
            return {'error': str(e)}
    
    def get_archive_metrics(self) -> Dict:
        """Get metrics about archived data"""
        print("\n💾 Collecting archive metrics...")
        
        url = f"{self.base_url}/v1/file/savedlist"
        
        try:
            response = requests.get(url, headers=self.headers, verify=False, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                archives = result.get('requestObj', {}).get('resources', [])
                
                by_user = defaultdict(list)
                total_size = 0
                
                for archive in archives:
                    user = archive.get('created_by', 'Unknown')
                    by_user[user].append({
                        'id': archive.get('id'),
                        'name': archive.get('name'),
                        'created_at': archive.get('created_at'),
                        'job_id': archive.get('job_id')
                    })
                
                print(f"   ✓ Found {len(archives)} archive files")
                
                return {
                    'total_archives': len(archives),
                    'by_user': dict(by_user),
                    'all_archives': archives
                }
            else:
                print(f"   ✗ Error: {response.status_code}")
                return {'error': response.text}
                
        except Exception as e:
            print(f"   ✗ Exception: {e}")
            return {'error': str(e)}
    
    def _calculate_summary(self, metrics: Dict) -> Dict:
        """Calculate summary statistics"""
        jobs = metrics.get('jobs', {})
        executions = metrics.get('executions', {})
        archives = metrics.get('archives', {})
        
        summary = {
            'total_jobs': jobs.get('total_jobs', 0),
            'total_executions': executions.get('total_runs', 0),
            'total_archives': archives.get('total_archives', 0),
            'success_rate': 0,
            'unique_users': len(jobs.get('by_user', {})),
            'avg_duration_seconds': 0,
            'oldest_archive_days': 0
        }
        
        # Calculate success rate
        total_runs = executions.get('total_runs', 0)
        if total_runs > 0:
            success_rate = (executions.get('successful_runs', 0) / total_runs) * 100
            summary['success_rate'] = round(success_rate, 2)
        
        # Calculate average duration
        if total_runs > 0:
            avg_duration = executions.get('total_duration_seconds', 0) / total_runs
            summary['avg_duration_seconds'] = round(avg_duration, 2)
        
        # Calculate oldest archive age
        all_archives = archives.get('all_archives', [])
        if all_archives:
            oldest_date = None
            for archive in all_archives:
                created_at = archive.get('created_at')
                if created_at:
                    try:
                        archive_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        if oldest_date is None or archive_date < oldest_date:
                            oldest_date = archive_date
                    except (ValueError, AttributeError):
                        continue
            
            if oldest_date:
                age_days = (datetime.now(oldest_date.tzinfo) - oldest_date).days
                summary['oldest_archive_days'] = age_days
        
        return summary
    
    def save_metrics(self, metrics: Dict, filename: str = 'bi_metrics.json'):
        """Save metrics to JSON file"""
        with open(filename, 'w') as f:
            json.dump(metrics, f, indent=2)
        print(f"\n💾 Metrics saved to {filename}")


def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("  IBM OPTIM ARCHIVE - BI DATA COLLECTOR")
    print("="*60 + "\n")
    
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
        print("❌ Error: .env file not found or incomplete")
        print("Please create a .env file in the project root with your credentials")
        return
    
    base_url = config['OPTIM_BASE_URL']
    username = config['OPTIM_USERNAME']
    password = config['OPTIM_PASSWORD']
    account_id = config.get('OPTIM_ACCOUNT_ID', '')
    
    # Get access token
    auth = OptimAuthHelper(base_url, username, password)
    access_token = auth.get_access_token()
    
    if not access_token:
        print("❌ Failed to retrieve access token")
        return
    
    print()
    
    # Collect metrics
    collector = ArchivalBICollector(
        base_url=base_url,
        access_token=access_token,
        account_id=account_id if account_id else None
    )
    
    metrics = collector.collect_all_metrics()
    
    # Save to file
    collector.save_metrics(metrics)
    
    # Print summary
    print("\n" + "="*60)
    print("  SUMMARY")
    print("="*60)
    summary = metrics.get('summary', {})
    print(f"\n📊 Total Jobs: {summary.get('total_jobs', 0)}")
    print(f"⚡ Total Executions: {summary.get('total_executions', 0)}")
    print(f"💾 Total Archives: {summary.get('total_archives', 0)}")
    print(f"👥 Unique Users/Business Units: {summary.get('unique_users', 0)}")
    print(f"✅ Success Rate: {summary.get('success_rate', 0)}%")
    print(f"⏱️  Average Duration: {summary.get('avg_duration_seconds', 0)} seconds")
    print()


if __name__ == "__main__":
    main()
