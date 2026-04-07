# Project Architecture & Refactoring Roadmap

## 1. Current File Inventory & Tasks

| File Path | Primary Task | Role |
| :--- | :--- | :--- |
| `routes/task_router.py` | CRUD operations for Task database records. | Endpoint / Controller |
| `routes/file_router.py` | CRUD operations for File metadata records. | Endpoint / Controller |
| `routes/user_router.py` | CRUD operations for User records. | Endpoint / Controller |
| `routes/query_router.py` | **Complex Orchestration**: Calls AI, loops through tools, and returns results. | Fat Controller |
| `routes/execute_router.py` | Direct manual execution of a specific tool. | Endpoint / Controller |
| `routes/tools_router.py` | Lists available AI tools in the registry. | Endpoint / Controller |
| `routes/server_router.py` | Basic health checks (DB connection). | Utility Endpoint |
| `services/file_tools.py` | Low-level OS interaction (scanning disk, file sizes, categories). | Utility Service |
| `services/mcp_server.py` | Registry for tools; coordinates `FileTools` for AI consumption. | Tool Orchestrator |
| `services/ai_data.py` | Wraps Google Gemini API; handles prompt engineering and JSON parsing. | AI Driver |

---

## 2. Current Architecture Overview
Your project currently follows a **Two-Tier Architecture**:
1.  **Route Layer (`routes/`)**: Handles HTTP requests, but also performs Database queries (SQLAlchemy) and coordinates AI business logic.
2.  **Infrastructure Layer (`services/`)**: Contains the "engines" (AI, File Scanner) but doesn't manage the database.

**Folders:**
- `routes/`: All entry points for the API.
- `services/`: Low-level logic for AI and File management.
- `models/`: Database table definitions.
- `schemas/`: Pydantic models for data validation.

---

## 3. Honest Assessment of Issues
While the code is clean and well-logged, there are three structural risks:

1.  **Fat Controllers (Route Overload)**: 
    - `query_router.py` contains a `for` loop that decides how tools are called. If you later want to call a tool via a background task or a different API, you'd have to copy-paste that loop. 
    - Logic like `if tool_name in mcp.tool_registry` belongs in a Service, not a Router.

2.  **Leaky Database Logic**: 
    - `file_router.py` and `task_router.py` call `db.query(File).all()` directly. The "Route" knows exactly how the database is structured. If you switch from SQLAlchemy to another ORM, you have to fix every single route file.

3.  **Synchronous Bottlenecks**:
    - `MCPServer` runs `analyze_folder()` on startup. If the folder is huge, the entire API server will hang or take minutes to start up.

---

## 4. How to Fix (The Strategy)
We need to move to a **Three-Layer Architecture**:
1.  **Routers**: Only handle HTTP (get data from request, call service, return status code).
2.  **Services (The Brain)**: Handle Business Logic. They combine AI + Tools + DB queries.
3.  **Repositories/Utilities**: Low-level drivers (Gemini API, File System, pure DB queries).

**Specific Changes:**
- Create a `TaskService` to handle DB operations for tasks.
- Move the "Tool Execution Loop" from `query_router.py` into the `MCPServer` or a new `QueryService`.
- Ensure Routers never call `db.query` directly.

---

## 5. Ideal File Locations (Target Structure)

This is where your files should be located after refactoring:

```text
File_management_system/
├── app.py                  # App entry & Dependency Injection
├── routes/                 # THIN LAYER (HTTP only)
│   ├── query_routes.py     # Just calls QueryService.process()
│   ├── task_routes.py      # Just calls TaskService.get_all()
│   └── ...
├── services/               # THE BRAIN (Business Logic)
│   ├── query_service.py    # NEW: Orchestrates AI + Tool Loop
│   ├── task_service.py     # NEW: Logic for Task DB/Management
│   ├── file_service.py     # NEW: Logic for File DB/Scanning
│   └── ai_handler.py       # Driver for Gemini
├── core/                   # INFRASTRUCTURE (Utilities)
│   ├── mcp_registry.py     # The tool registration system
│   └── file_utils.py       # Pure disk scanning (OS logic)
├── models/                 # DB Models (SQLAlchemy)
└── schemas/                # Data Models (Pydantic)
```

### Summary of Migration
- **Move** `file_tools.py` logic into `core/file_utils.py`.
- **Move** DB queries from `task_router.py` into `services/task_service.py`.
- **Move** AI-Tool coordination from `query_router.py` into `services/query_service.py`.

By doing this, your Routers will become 5-10 lines of code each, making the system incredibly easy to test and expand.

---
