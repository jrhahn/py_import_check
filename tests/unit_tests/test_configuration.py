from __future__ import annotations

from pathlib import Path

import pytest

from import_check.import_check_configuration import load


@pytest.fixture
def path_test_resources():
    yield Path(__file__).parents[1] / "resources" / "configuration"


def test_configuration_missing():
    with pytest.raises(FileNotFoundError):
        load(Path("does") / "not" / "exist")


def test_configuration(path_test_resources: Path):
    config = load(path_test_resources / ".import_check.toml")

    assert len(config) == 1
    assert "package_2" in config
    assert "forbidden_imports" in config["package_2"]
    assert isinstance(config["package_2"]["forbidden_imports"], list)
    assert len(config["package_2"]) == 1
    assert isinstance(config["package_2"]["forbidden_imports"][0], str)
