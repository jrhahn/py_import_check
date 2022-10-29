from __future__ import annotations

from pathlib import Path

import pytest

from import_check.main import extract_module


def test_extract_module():
    module = extract_module(file_name=Path("module") / "path1" / "path")

    assert module == "module"


def test_extract_module_path_not_existent():
    with pytest.raises(IndexError):
        extract_module(file_name=Path(""))
