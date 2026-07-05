import shutil
import tempfile
from pathlib import Path

from utils.sorting_helper import start_sort


def test_start_sort_handles_dict_rows_and_moves_files(tmp_path):
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    source_file = source_dir / "notes.txt"
    source_file.write_text("hello", encoding="utf-8")

    result = start_sort([
        {"path": str(source_file), "extension": "txt"}
    ])

    assert result["moved"][0]["name"] == "notes.txt"
    assert not source_file.exists()
    assert (source_dir / "text" / "notes.txt").exists()

    shutil.rmtree(tmp_path, ignore_errors=True)
