import importlib
import sys
from pathlib import Path
import pytest
import pathlib


@pytest.fixture
def transittool_module(tmp_path, monkeypatch):
    """
    Re-import the transittool module with Path.home() patched to tmp_path so
    DATA_DIR is created under the temporary test directory
    """
    # Patch pathlib.Path.home to return tmp_path
    monkeypatch.setattr(pathlib.Path, "home", lambda self=None: tmp_path)
    # Ensure fresh import
    if "transittool" in sys.modules:
        del sys.modules["transittool"]
    module = importlib.import_module("transittool")
    importlib.reload(module)
    return module


@pytest.fixture
def sample_csv_path():
    """
    Return the first CSV file found in the tests/ directory
    """
    tests_dir = Path(__file__).parent
    csv_files = list(tests_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError("No CSV file found in tests/. Add your sample Compass CSV there.")
    return csv_files[0]