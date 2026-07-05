from utils import SessionLocal
from services import DBService
from core import MCPRegistry
from pathlib import Path

db = SessionLocal()
print(MCPRegistry(db,1).auto_sort_files("E:\test_folder"))
# print(DBService.auto_sort_files(db,1,r"E:/test_folder"))