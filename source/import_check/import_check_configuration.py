import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict


@dataclass
class ModuleConfiguration:
    module: str
    forbidden_imports: List[str]

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            module=data["module"],
            forbidden_imports=data["forbidden_imports"],
        )


@dataclass
class ImportCheckConfiguration:
    modules: List[ModuleConfiguration]

    @staticmethod
    def load(path_config_file: Path):
        if not (path_config_file.exists()):
            raise ValueError(f"Configuration file not found in {path_config_file}")

        with open(path_config_file) as fp:
            config = json.load(fp=fp)

        return ImportCheckConfiguration.from_dict(data=config)

    @classmethod
    def from_dict(cls, data: List[Dict]):
        return ImportCheckConfiguration(
            modules=[ModuleConfiguration.from_dict(entry) for entry in data],
        )
