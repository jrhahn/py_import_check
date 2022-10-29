from __future__ import annotations

from pathlib import Path

import pytest

from import_check.main import check_all_files


@pytest.fixture
def path_test_resources():
    yield Path(__file__).parents[1] / "resources" / "source"


def test_check_all_files(path_test_resources: Path, mocker):
    mocker.patch("import_check.main.extract_module", return_value="package_1")

    exit_code = check_all_files(
        config={"package_1": {"forbidden_imports": []}},
        file_names=[path_test_resources / "package_1" / "code_1.py"],
    )

    assert exit_code == 0


def test_check_all_files_failed(path_test_resources: Path, mocker):
    mocker.patch("import_check.main.extract_module", return_value="package_1")

    exit_code = check_all_files(
        config={"package_1": {"forbidden_imports": ["json"]}},
        file_names=[path_test_resources / "package_1" / "code_1.py"],
    )

    assert exit_code == 1
