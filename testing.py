# from core import FileUtils 
from utils import SessionLocal
from services import DBService
from core import MCPRegistry


print(MCPRegistry(SessionLocal(),1).get_oldest_file())
print(MCPRegistry(SessionLocal(),1).get_newest_file())


# result = DBService.get_oldest_file(SessionLocal(),1)

# print(result)
