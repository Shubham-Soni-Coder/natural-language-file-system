from utils import SessionLocal
from pathlib import Path
from services import DBService
from core import MCPRegistry

db = SessionLocal()

target_folder = "E:/"

print(MCPRegistry(db,1).get_largest_folder(target_folder))
print(MCPRegistry(db,1).get_largest_folders(target_folder,8))

