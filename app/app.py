from fastapi import FastAPI
from routes.tools_route import route as tools_router
from routes.execute_route import route as execute_router
from routes.query_route import route as query_router

app = FastAPI(title="AI File Management System")

# Register individual specialized routers
app.include_router(tools_router)
app.include_router(execute_router)
app.include_router(query_router)
