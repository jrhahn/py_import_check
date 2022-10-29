from __future__ import annotations

from pathlib import Path

import pytest

from import_check.main import check_dependencies


@pytest.fixture
def path_test_resources():
    yield Path(__file__).parents[1] / "resources" / "source"


def test_check_dependencies_pass(path_test_resources: Path):
    passed = check_dependencies(
        file_name=path_test_resources / "package_1" / "code_1.py",
        forbidden_imports=["package_1"],
    )

    assert passed


def test_check_dependencies_fail(path_test_resources: Path):
    passed = check_dependencies(
        file_name=path_test_resources / "package_1" / "code_1.py",
        forbidden_imports=["package_2"],
    )

    assert not passed


def test_check_dependencies_unknown_import(path_test_resources: Path):
    passed = check_dependencies(
        file_name=path_test_resources / "package_1" / "code_1.py",
        forbidden_imports=["<unknown>"],
    )

    assert passed
