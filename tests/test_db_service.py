import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils import Base
from models import File, User
from services import DBService

@pytest.fixture
def db_session():
    # Setup in-memory SQLite database for testing database service logic
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create a test user
    user = User(id=1, name="Test User", email="test@example.com")
    session.add(user)
    session.commit()

    try:
        yield session
    finally:
        session.close()

def test_get_total_files(db_session):
    # Add files
    file1 = File(user_id=1, name="a.txt", path="a.txt", size=100, is_folder=False)
    file2 = File(user_id=1, name="b.png", path="b.png", size=200, is_folder=False)
    file3 = File(user_id=1, name="subfolder", path="subfolder", size=0, is_folder=True)
    db_session.add_all([file1, file2, file3])
    db_session.commit()

    count = DBService.get_total_files(db_session, user_id=1)
    assert count == 2

def test_get_total_size(db_session):
    file1 = File(user_id=1, name="a.txt", path="a.txt", size=100, is_folder=False)
    file2 = File(user_id=1, name="b.png", path="b.png", size=250, is_folder=False)
    db_session.add_all([file1, file2])
    db_session.commit()

    size = DBService.get_total_size(db_session, user_id=1)
    assert size == 350

def test_get_largest_files(db_session):
    file1 = File(user_id=1, name="small.txt", path="small.txt", size=100, is_folder=False)
    file2 = File(user_id=1, name="large.zip", path="large.zip", size=5000, is_folder=False)
    file3 = File(user_id=1, name="medium.png", path="medium.png", size=1000, is_folder=False)
    db_session.add_all([file1, file2, file3])
    db_session.commit()

    largest_list = DBService.get_largest_files(db_session, user_id=1, limit=2)
    assert len(largest_list) == 2
    assert largest_list[0].name == "large.zip"
    assert largest_list[1].name == "medium.png"

    # Test single get_largest_file helper
    largest_single = DBService.get_largest_file(db_session, user_id=1)
    assert largest_single.name == "large.zip"

def test_get_folder_count(db_session):
    file1 = File(user_id=1, name="a.txt", path="a.txt", size=100, is_folder=False)
    folder1 = File(user_id=1, name="docs", path="docs", size=0, is_folder=True)
    folder2 = File(user_id=1, name="images", path="images", size=0, is_folder=True)
    db_session.add_all([file1, folder1, folder2])
    db_session.commit()

    count = DBService.get_folder_count(db_session, user_id=1)
    assert count == 2
