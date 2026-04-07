from app import DataBaseDep
from fastapi import APIRouter
from schemas import TaskCreate,TaskRespone
from services import TaskService
from utils import main_logger as logger 

route = APIRouter()

# @route.get("/tasks/get_child")
# def get_child_tasks(db:DataBaseDep,parent_id:int):
#     logger.info("Fetching all child taks")
#     return TaskService.get_by_parent(db, parent_id)

@route.post("/tasks",response_model=TaskRespone)
def create_task(db:DataBaseDep,data:TaskCreate):
    logger.info("Creating task record %s for user %s",data.task_type,data.user_id)
    return TaskService.create(db, data)
