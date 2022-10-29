from pathlib import Path
from typing import List, Dict

import toml

ModulesType = Dict[str, List[str]]


def load(path_config_file: Path) -> ModulesType:
    if not (path_config_file.exists()):
        raise ValueError(f"Configuration file not found in {path_config_file}")

    with open(path_config_file) as fp:
        config = toml.load(f=fp)

    return config
