from utils import SessionLocal
from core import MCPRegistry,FileUtils
from services import DBService

# print(MCPRegistry(SessionLocal(),1).get_summary())
# print(DBService.get_summary_stats(SessionLocal(),1))
print(DBService.get_all_category_count(SessionLocal(),1))
