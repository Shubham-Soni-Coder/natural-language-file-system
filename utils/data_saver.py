from utils import main_logger as logger 
from core import FileUtils
import requests

def save_file_data():
    logger.info("Adding file: %s for user %s", name, user_id)
    response = requests.post(
        f"{SERVER_URL}/files", json={"name":name,"path":path,"size":size,"mime_type":mime_type,"extension":extension,"hash":hash,"user_id":user_id,"status":status}
    )
    print(response.text)


SERVER_URL = "http://127.0.0.1:8000"

