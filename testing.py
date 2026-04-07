from services import TaskService as Ts
from utils import SessionLocal


# temp db 
db = SessionLocal()


# get child tasks 
# print(TaskService.get_child_tasks(db,1))

print(Ts.update_task(db,1,"complete"))