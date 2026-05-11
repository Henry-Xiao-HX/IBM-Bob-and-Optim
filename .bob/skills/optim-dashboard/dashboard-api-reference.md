# Dashboard API Reference

## Overview

The dashboard provides RESTful API endpoints for accessing Optim Archive metrics. All endpoints return JSON data.

## Base URL

```
http://localhost:5001
```

## Endpoints

### GET /api/metrics

Get all metrics in a single response.

**Query Parameters:**
- `refresh` (optional): Set to `true` to force cache refresh

**Response:**
```json
{
  "summary": {
    "total_jobs": 10,
    "total_executions": 45,
    "total_archives": 8,
    "success_rate": 95.5
  },
  "jobs": {
    "total": 10,
    "by_status": {...},
    "by_user": {...}
  },
  "executions": {
    "total": 45,
    "by_status": {...},
    "by_user": {...}
  },
  "archives": {
    "total": 8,
    "by_user": {...}
  }
}
```

### GET /api/summary

Get summary statistics only.

**Response:**
```json
{
  "total_jobs": 10,
  "total_executions": 45,
  "total_archives": 8,
  "success_rate": 95.5,
  "last_updated": "2024-01-15T10:30:00Z"
}
```

### GET /api/jobs

Get job-related metrics.

**Response:**
```json
{
  "total": 10,
  "by_status": {
    "completed": 8,
    "failed": 1,
    "running": 1
  },
  "by_user": {
    "user1": [...],
    "user2": [...]
  },
  "recent": [...]
}
```

### GET /api/executions

Get execution history metrics.

**Response:**
```json
{
  "total": 45,
  "by_status": {
    "FINISHED": 43,
    "FAILED": 2
  },
  "by_user": {
    "user1": {
      "runs": 20,
      "success": 19,
      "failed": 1
    }
  },
  "recent": [...]
}
```

### GET /api/archives

Get archive file metrics.

**Response:**
```json
{
  "total": 8,
  "by_user": {
    "user1": [...],
    "user2": [...]
  },
  "total_size": "1.2 GB",
  "recent": [...]
}
```

### GET /api/business-units

Get business unit breakdown.

**Response:**
```json
[
  {
    "business_unit_id": 1,
    "name": "user1",
    "jobs": 5,
    "executions": 20,
    "archives": 4,
    "success_rate": 95.0
  }
]
```

## Caching

- Default cache duration: 5 minutes
- Force refresh: Add `?refresh=true` to any endpoint
- Cache is shared across all endpoints

## Error Responses

### 500 Internal Server Error
```json
{
  "error": "Failed to authenticate"
}
```

### 404 Not Found
```json
{
  "error": "Endpoint not found"
}
```

## Usage Examples

### JavaScript (Fetch API)
```javascript
// Get all metrics
fetch('/api/metrics')
  .then(response => response.json())
  .then(data => console.log(data));

// Force refresh
fetch('/api/metrics?refresh=true')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Python (requests)
```python
import requests

# Get summary
response = requests.get('http://localhost:5001/api/summary')
data = response.json()
print(data)
```

### cURL
```bash
# Get all metrics
curl http://localhost:5001/api/metrics

# Force refresh
curl http://localhost:5001/api/metrics?refresh=true

# Get summary only
curl http://localhost:5001/api/summary

# Get business units
curl http://localhost:5001/api/business-units
```