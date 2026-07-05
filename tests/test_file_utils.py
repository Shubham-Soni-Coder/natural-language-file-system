import pytest
from pathlib import Path
from core.file_utils import FileUtils

def test_get_extension():
    # Instantiate FileUtils on current directory since we just need the helpers
    utils = FileUtils(str(Path(__file__).parent))
    assert utils.get_extension(Path("hello.py")) == "py"
    assert utils.get_extension(Path(".gitignore")) == "gitignore"
    assert utils.get_extension(Path("archive.tar.gz")) == "gz"
    assert utils.get_extension(Path("no_extension")) == ""

def test_get_mime_type():
    utils = FileUtils(str(Path(__file__).parent))
    assert utils.get_mime_type(Path("test.txt")) == "text/plain"
    assert utils.get_mime_type(Path("test.png")) == "image/png"

def test_get_file_hash_and_size(tmp_path):
    test_file = tmp_path / "test.txt"
    content = "Hello, world!"
    test_file.write_text(content, encoding="utf-8")

    utils = FileUtils(str(tmp_path))
    assert utils.get_file_size(test_file) == len(content.encode("utf-8"))
    
    file_hash = utils.get_file_hash(test_file, enable=True)
    assert file_hash is not None
    assert len(file_hash) == 64 # SHA-256 returns 64 character hex string

def test_scan_ignores_skip_folders(tmp_path):
    # Setup folders
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (src_dir / "code.py").write_text("print(1)", encoding="utf-8")

    skip_dir = tmp_path / "__pycache__"
    skip_dir.mkdir()
    (skip_dir / "cache.pyc").write_text("cached", encoding="utf-8")

    utils = FileUtils(str(tmp_path))
    scan_results = list(utils.scan(include_hash=False))

    # Should find code.py and src folder, but ignore __pycache__ and cache.pyc
    file_names = [res["name"] for res in scan_results]
    assert "code.py" in file_names
    assert "src" in file_names
    assert "__pycache__" not in file_names
    assert "cache.pyc" not in file_names
