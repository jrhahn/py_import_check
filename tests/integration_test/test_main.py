from __future__ import annotations

from pathlib import Path

import pytest

from import_check.main import main


@pytest.fixture
def path_test_resources():
    yield Path(__file__).parents[1] / "resources"


def test_main_passed(path_test_resources: Path, mocker):
    mocker.patch("import_check.main.extract_module", return_value="package_1")

    passed = main(
        args=[
            "--config",
            f"{path_test_resources / 'configuration' / '.import_check.toml'}",
            f"{path_test_resources / 'source' / 'package_1' / 'code_1.py'}",
        ]
    )

    assert not passed


def test_main_not_passed(path_test_resources: Path, mocker):
    mocker.patch("import_check.main.extract_module", return_value="package_1")

    passed = main(
        args=[
            "--config",
            f"{path_test_resources / 'configuration' / '.import_check.toml'}",
            f"{path_test_resources / 'source' / 'package_1' / 'code_1.py'}",
            f"{path_test_resources / 'source' / 'package_2' / 'code_1.py'}",
        ]
    )

    assert not passed
