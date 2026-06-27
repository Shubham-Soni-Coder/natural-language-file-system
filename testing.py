from services import DBService
from utils import SessionLocal
from core import MCPRegistry

# print(DBService.get_largest_files(SessionLocal(),1,10))
print(MCPRegistry(SessionLocal(),1).get_largest_files(10))