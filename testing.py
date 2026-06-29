# from core import FileUtils 
from utils import SessionLocal
from services import DBService
from core import MCPRegistry

db = SessionLocal()

print(MCPRegistry(db,1).get_file_type_distribution())