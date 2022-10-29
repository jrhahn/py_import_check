import argparse
from pathlib import Path
from typing import Dict, List, Optional
from loguru import logger  # type: ignore

from import_check.dependency import analyse

from source.import_check.import_check_configuration import (
    ImportCheckConfiguration,
    ModuleConfiguration,
)


def reshape(rules: List[Dict]) -> Dict:
    return {rule.pop("module"): rule for rule in rules}


def check_files_in_module(
    path_module: Path,
    forbidden_imports: List[str],
) -> bool:
    status = True

    for file_name in path_module.rglob("*.py"):
        logger.info(f"Checking {file_name}..")
        dependencies = analyse(file=file_name)

        for d in dependencies:
            status_ = d in forbidden_imports

            status = status_ and status

            if not status_:
                logger.error(f"{file_name} should not import from {forbidden_imports}")

    return status


def check_modules(modules: List[ModuleConfiguration]) -> bool:
    status = True

    for module_config in modules:
        status = status and check_files_in_module(
            path_module=Path(module_config.module),
            forbidden_imports=module_config.forbidden_imports,
        )

    return status


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()

    path_config_file = args.config

    if path_config_file is None:
        path_config_file = ".import_check_config.json"

    import_check_config = ImportCheckConfiguration.load(
        path_config_file=path_config_file
    )

    return check_modules(modules=import_check_config.modules)


if __name__ == "__main__":
    raise SystemExit(main())
