from fastapi import FastAPI
from routes import tools_router, execute_router, query_router, server_router, user_router, file_router
from utils import main_logger as logger
from app import add_exception_handlers

app = FastAPI(title="AI File Management System")
logger.info("FastAPI application initialized")

# Register individual specialized routers
app.include_router(tools_router)
app.include_router(execute_router)
app.include_router(query_router)
app.include_router(server_router)
app.include_router(user_router)
app.include_router(file_router)

# Initialize global automated error handling
add_exception_handlers(app)
