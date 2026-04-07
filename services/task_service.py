from sqlalchemy.orm import Session
from models import Task
from schemas import TaskCreate

class TaskService:
    @staticmethod
    def get_child_tasks(db: Session, parent_id: int):
        """Fetches all child tasks for a given parent task ID."""
        return db.query(Task).filter(Task.parent_task_id == parent_id).all()

    @staticmethod
    def create(db: Session, data: TaskCreate):
        """Creates a new task record in the database."""
        task = Task(
            user_id=data.user_id,
            task_type=data.task_type,
            input_data=data.input_data,
            parent_task_id=data.parent_task_id,
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    
    @staticmethod 
    def get_pending_parent(db:Session):
        """Fetches all the pending tasks for specfic parent""" 
        return db.query(Task).filter(
            Task.parent_task_id == None,
            Task.status == "pending"
        ).first()
    
    @staticmethod
    def update_task(db:Session,task_id:int,status:str,result=None,error=None):
        task = db.query(Task).filter(Task.id==task_id).first()

        if not task:
            return None
        
        task.status = status

        if result is not None:
            task.result = result
        
        if error is not None:
            task.error = error 
        
        db.commit()
        db.refresh(task)

        return task
