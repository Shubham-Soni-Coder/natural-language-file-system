from app import DataBaseDep
from fastapi import APIRouter
from schemas import TaskCreate,TaskRespone
from models import Task
from utils import main_logger as logger 

route = APIRouter()

@route.get("/tasks/get_child")
def get_child_tasks(db:DataBaseDep,parent_id:int):
    logger.info("Fetching all child taks")
    child_task = db.query(Task).filter(Task.parent_task_id==parent_id).all()
    logger.debug("Returned %s child tasks",len(child_task))

@route.post("/tasks",response_model=TaskRespone)
def create_task(db:DataBaseDep,data:TaskCreate):
    logger.info("Creating task record %s for user %s",data.task_type,data.user_id)
    task = Task(
        user_id=data.user_id,
        task_type=data.task_type,
        input_data=data.input_data,
        parent_task_id=data.parent_task_id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    logger.debug("Created task id: %s",task.id)
    return task

