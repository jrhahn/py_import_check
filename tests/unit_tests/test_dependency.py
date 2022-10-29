from __future__ import annotations

from pathlib import Path

import pytest

from import_check.dependency import analyse


@pytest.fixture
def path_test_resources():
    yield Path(__file__).parents[1] / "resources" / "source"


def test_analyse(path_test_resources: Path):
    packages = analyse(file=path_test_resources / "package_1" / "code_1.py")

    assert len(packages) >= 2
    assert "package_2" in packages
    assert "json" in packages


def test_analyse_empty(path_test_resources: Path):
    packages = analyse(file=path_test_resources / "package_1" / "__init__.py")

    assert len(packages) == 0
