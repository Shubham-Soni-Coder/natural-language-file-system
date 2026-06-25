# Project Flow

## Start Router

### Purpose

Handle the startup scan operation and store scanned file metadata in the database.

### Trigger

Application Startup Event

### Flow

* Server start
* Create database session
* Create `FileUtils` object
* `scan()`
* `FileService.ingest()`
* Store file metadata in database
* Finish

### Output

* File metadata stored in database

---

## Tools Router

### Purpose

Retrieve all available tools registered in the MCP Registry.

### Endpoint

`GET /tools`

### Input

* MCP Registry dependency

### Flow

* Client request
* `get_tools()`
* `mcp.get_tools()`
* Retrieve registered tools
* Return tool list
* Finish

### Output

```json
{
  "status": "success",
  "tools": []
}
```

---

## Execute Tool

### Purpose

Execute a tool from the MCP Registry using the provided tool name and arguments.

### Endpoint

`POST /execute`

### Input

* `tool_name`
* `arguments`
* MCP Registry dependency

### Flow

* Client request
* `execute_tools()`
* `mcp.execute_tool(tool_name, arguments)`
* Find tool in registry
* Execute tool
* Get result
* Return response

### Output

```json
{
  "status": "success",
  "data": {}
}
```

---

## Query Router

### Purpose

Handle natural language user queries and execute the selected tools.

### Endpoint

`POST /query`

### Input

* `query: str`

### Dependencies

* `QueryService`
* `AiDriver`
* `MCPRegistry`
* Database session

### Flow

* User query
* `process_query()`
* `QueryService.process_query()`
* `mcp_registry.get_tools()`
* Get available tools
* `ai_handler.run_ai(query, tools)`
* AI selects tool(s)
* Extract `tool_name` and arguments
* Get all tools details from `db_serice.py`
* Save in `MCPRegistry.tool_registry`
* Validate tool exists in `MCPRegistry`
* `mcp_registry.execute_tool()`
* Execute selected tool
* Cell specfic function from `db_service.py` 
* Collect results
* Return response

### Output

```json
[
  {
    "tool": "tool_name",
    "result": {}
  }
]
```

### Possible Errors

* `400` : Could not understand query
* Tool not found
* Tool execution failed

---

## Server Router

### Purpose

Return the current database connection status.

### Endpoint

`GET /database`

### Input

* None

### Flow

* Client request
* `read_db()`
* Return database status

### Output

```json
{
  "connection": true,
  "message": "DB connected"
}
```

---

## User Router

### Purpose

Create and retrieve user records from the database.

### Endpoints

* `POST /user`
* `GET /user`

### POST /user

#### Input

* `name`
* `email`
* Database session

#### Flow

* Client request
* Validate `UserCreate` schema
* Create user object
* Save user to database
* Commit changes
* Refresh user
* Return user

#### Output

* `UserResponse`

### GET /user

#### Input

* Database session

#### Flow

* Client request
* `get_user()`
* `UserService.get_all()`
* Query user table
* Get all users
* Return user list

#### Output

* `List[User]`

---

## File Router

### Purpose

Create and retrieve file records from the database using `FileService`.

### Endpoints

* `GET /files`
* `POST /files`
* `POST /user/{user_id}/files`

### GET /files

#### Input

* Database session

#### Flow

* Client request
* `get_files()`
* `FileService.get_all()`
* Query database
* Get all files
* Return files

#### Output

* `List[File]`

### POST /files

#### Input

* `request: FileCreate`
* Database session

#### Flow

* Client request
* `create_files()`
* Validate `FileCreate` schema
* `FileService.create()`
* Create file record
* Save to database
* Return file

#### Output

* `FileResponse`

### POST /user/{user_id}/files

#### Input

* `user_id: int`
* Database session

#### Flow

* Client request
* `get_user_files()`
* `FileService.get_by_user()`
* Query database
* Filter by `user_id`
* Return user files

#### Output

* `List[File]`

---

## Task Router

### Purpose

Create task records using `TaskService`.

### Endpoint

`POST /tasks`

### Input

* Database session
* `TaskCreate`

### Flow

* Client request
* `create_task()`
* Validate task schema
* `TaskService.create()`
* Create task object
* Save to database
* Return task

### Output

* `TaskResponse`

---

## Exception Handlers

### Purpose

Handle database integrity errors and return user-friendly error messages.

### Trigger

IntegrityError Exception

### Flow

* Application start
* `add_exception_handlers(app)`
* Register `IntegrityError` handler
* Wait for exception
* `IntegrityError` raised
* Log technical error
* Create JSON response
* Return HTTP 400 response

### Output

```json
{
  "error": "Database Error",
  "detail": "This record (e.g., email or filename) already exists in our system."
}
```
