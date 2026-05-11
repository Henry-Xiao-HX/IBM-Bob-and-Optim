# Optim Archive API Endpoints Reference

## Base URL

```
https://your-optim-server:7725/optim
```

## Authentication

### Get Access Token

**Endpoint:** `POST /v1/auth/login`

**Request Body:**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 86400
}
```

**Note:** The toolkit handles this automatically via `auth_helper.py`

## Job Management

### List All Jobs

**Endpoint:** `GET /v1/job/savedlist`

**Query Parameters:**
- `worksheet_type` (optional): Filter by type (e.g., "archive")
- `src_conn_name` (optional): Filter by source connection

**Response:**
```json
{
  "requestObj": {
    "total_count": 10,
    "resources": [
      {
        "id": "job-123",
        "name": "Archive Job 1",
        "description": "Archive customer data",
        "created_at": "2024-01-01T00:00:00Z",
        "last_run_status": "FINISHED",
        "src_conn_name": "source_db",
        "dest_conn_name": "archive_storage"
      }
    ]
  }
}
```

### Get Job Details

**Endpoint:** `GET /v1/job/details/{job_id}`

**Response:**
```json
{
  "id": "job-123",
  "name": "Archive Job 1",
  "description": "Archive customer data",
  "flow_id": "flow-456",
  "src_conn_name": "source_db",
  "dest_conn_name": "archive_storage",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-15T00:00:00Z",
  "pipeline_flow": {
    // Complete pipeline configuration
  }
}
```

### Get Job Execution Status

**Endpoint:** `GET /v1/job/spark/status/{job_id}`

**Query Parameters:**
- `limit` (optional): Number of runs to return (default: 25)

**Response:**
```json
[
  {
    "spark_app_id": "app-20240115-001",
    "submission_id": "sub-001",
    "status": "FINISHED",
    "start_time": "2024-01-15T10:00:00Z",
    "completion_time": "2024-01-15T10:30:00Z",
    "duration_seconds": 1800,
    "error_message": null
  }
]
```

## Archive File Access

### List Archive Files

**Endpoint:** `GET /v1/file/savedlist`

**Response:**
```json
{
  "requestObj": {
    "total_count": 8,
    "resources": [
      {
        "id": "archive-789",
        "name": "Customer Archive 2024-01",
        "job_id": "job-123",
        "created_at": "2024-01-15T10:30:00Z",
        "status": "AVAILABLE"
      }
    ]
  }
}
```

### Get Archive Schemas

**Endpoint:** `GET /v1/file/schemas?id={job_id}`

**Response:**
```json
[
  {
    "name": "public",
    "tables": [
      "customers",
      "orders",
      "products"
    ]
  }
]
```

### Get Table Metadata

**Endpoint:** `GET /v1/file/schemas/{schema_name}/tables/{table_name}?id={job_id}`

**Response:**
```json
{
  "schema": "public",
  "table": "customers",
  "row_count": 50000,
  "last_collection_time": "2024-01-15T10:30:00Z",
  "columns": [
    {
      "name": "customer_id",
      "type": "INTEGER",
      "precision": 10,
      "nullable": false,
      "primary_key": true
    }
  ]
}
```

### Get Table Data

**Endpoint:** `GET /v1/file/schemas/{schema_name}/tables/{table_name}/data?id={job_id}`

**Query Parameters:**
- `limit` (optional): Number of rows (default: 100)
- `offset` (optional): Skip rows for pagination (default: 0)

**Response:**
```json
{
  "columns": [
    {"name": "customer_id", "type": "INTEGER"},
    {"name": "customer_name", "type": "VARCHAR"}
  ],
  "rows": [
    {"customer_id": 1, "customer_name": "John Doe"}
  ],
  "total_count": 50000,
  "offset": 0,
  "limit": 100
}
```

## Headers

All API requests require:

```
Authorization: Bearer {access_token}
Content-Type: application/json
```

Optional for multi-tenant environments:

```
account-id: {your_account_id}
```

## Error Responses

### 401 Unauthorized
```json
{
  "error": "Invalid or expired token"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "message": "Detailed error message"
}