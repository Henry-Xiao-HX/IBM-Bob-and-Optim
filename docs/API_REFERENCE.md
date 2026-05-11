# Archival Job Details & Metadata Access

## Available Endpoints for Job Details

### 1. **List All Saved Jobs**
- **Endpoint**: `GET /v1/job/savedlist`
- **Purpose**: Retrieve a list of all your archival jobs
- **Query Parameters**:
  - `worksheet_type`: Filter by type (e.g., "archive")
  - `src_conn_name`: Filter by source connection name
- **Returns**: Job metadata including:
  - Job ID, name, description
  - Creation/update timestamps
  - Source/target connection details
  - Last run status and timestamp
  - Flow ID and revision

### 2. **Get Specific Job Details**
- **Endpoint**: `GET /v1/job/details/{id}`
- **Purpose**: Retrieve complete details for a specific job
- **Returns**: Full job configuration including:
  - Pipeline configuration (tables, schemas, operations)
  - Source and destination connection IDs
  - User information (creator, timestamps)
  - Complete pipeline-flow-v3 JSON structure

### 3. **Get Job Run Status**
- **Endpoint**: `GET /v1/job/spark/status/{id}`
- **Purpose**: View execution history and status
- **Query Parameters**:
  - `limit`: Number of prior runs to retrieve (default: 25)
- **Returns**: Array of run statuses with:
  - Spark application ID and submission ID
  - Start/completion timestamps
  - Duration in seconds
  - Status (FINISHED, FAILED, RUNNING)
  - Error messages (if failed)

### 4. **Get Process Report**
- **Endpoint**: `GET /v1/job/report/spark_app_id/{spark_app_id}/flow_id/{flow_id}`
- **Purpose**: Detailed execution report for completed jobs
- **Returns**:
  - Total records processed, filtered, masked
  - Per-table statistics
  - Execution time
  - Processing status

## Archive File Metadata Access

### 5. **List Saved Archive Flows**
- **Endpoint**: `GET /v1/file/savedlist`
- **Returns**: All archive files with metadata:
  - Archive ID, name, flow information
  - Access definition details
  - Creation timestamp and user
  - Job ID and submission ID
  - Status

### 6. **Get Archive File Details**
- **Endpoint**: `GET /v1/file/job?id={job_id}`
- **Returns**: Complete archive file metadata including:
  - Full pipeline-flow-v3 structure
  - Table schemas and configurations
  - Connection profiles used

### 7. **Get Archive Schemas**
- **Endpoint**: `GET /v1/file/schemas?id={job_id}`
- **Returns**: Schema structure of archived data:
  - List of schemas
  - Tables within each schema

### 8. **Get Archive Table Details**
- **Endpoint**: `GET /v1/file/schemas/{schema_name}/tables/{table_name}?id={job_id}`
- **Returns**: Detailed table metadata:
  - Column definitions (names, types, precision)
  - Primary key information
  - Row counts and statistics
  - Last collection timestamp

### 9. **Get Archive Table Data**
- **Endpoint**: `GET /v1/file/schemas/{schema_name}/tables/{table_name}/data?id={job_id}`
- **Query Parameters**:
  - `offset`: Skip rows (pagination)
  - `limit`: Number of rows to return (default: 100)
- **Returns**: Actual archived data rows with column definitions

## Metadata Export Capabilities

**Direct Export**: The API does not provide a dedicated "export metadata" endpoint. However, you can:

1. **Programmatic Export**: Use the API endpoints above to retrieve metadata in JSON format and export it programmatically
2. **Available Metadata Formats**: All responses are in JSON format (application/json)
3. **Comprehensive Data**: You can retrieve:
   - Job configurations (pipeline-flow-v3 JSON)
   - Execution history and statistics
   - Schema definitions
   - Table structures and data samples

## Authentication Required

All endpoints require:
- **Header**: `Authorization: Bearer [access_token]`
- **Optional Header**: `account-id` for multi-tenant environments

## Example Workflow

```bash
# 1. List all archive jobs
GET /v1/job/savedlist?worksheet_type=archive

# 2. Get specific job details
GET /v1/job/details/{job_id}

# 3. Get execution history
GET /v1/job/spark/status/{job_id}?limit=10

# 4. Get archive file metadata
GET /v1/file/job?id={job_id}

# 5. Browse archive schemas
GET /v1/file/schemas?id={job_id}

# 6. View table details
GET /v1/file/schemas/public/tables/customers?id={job_id}

# 7. Sample archived data
GET /v1/file/schemas/public/tables/customers/data?id={job_id}&limit=100
```

## Key Points

✅ **Comprehensive metadata access** through multiple endpoints
✅ **Execution history** with detailed run statistics
✅ **Schema browsing** capabilities for archived data
✅ **Data sampling** to verify archive contents
❌ **No single "export all metadata" endpoint** - requires multiple API calls
✅ **JSON format** for all responses - easily parseable for export