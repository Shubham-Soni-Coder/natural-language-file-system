from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from utils.logging_config import main_logger as logger

def add_exception_handlers(app: FastAPI):
    @app.exception_handler(IntegrityError)
    async def integrity_exception_handler(request: Request, exc: IntegrityError):
        # SERVER: Log the full technical detail including the DB constraint that failed
        # This will show up in your terminal and application.log
        logger.error(f"Database Integrity Violation: {str(exc.orig)}")

        # CLIENT: Send a clean, helpful message to the user terminal
        return JSONResponse(
            status_code=400,
            content={
                "error": "Database Error",
                "detail": "This record (e.g., email or filename) already exists in our system."
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        # SERVER: Log the full traceback for any unexpected crash
        logger.exception("An unhandled exception occurred in the application.")

        # CLIENT: Hide technical details to prevent security leaks
        return JSONResponse(
            status_code=500,
            content={"detail": "An internal server error occurred. Our team has been notified."},
        )