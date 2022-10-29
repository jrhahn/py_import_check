import argparse
import logging
from pathlib import Path
from typing import List, Dict

from import_check.dependency import analyse
from import_check.import_check_configuration import load

logger = logging.getLogger(__name__)


def extract_module(file_name: Path) -> str:
    return file_name.parts[0]


def check_dependencies(
        file_name: Path,
        forbidden_imports: List[str],
) -> bool:
    passed = True

    logger.info(f"Checking {file_name}..")
    dependencies = analyse(file=file_name)

    for d in dependencies:
        passed_ = d not in forbidden_imports

        if not passed_:
            logger.info(f"{file_name} should not import from {forbidden_imports}")

        passed = passed_ and passed

    return passed


def check_all_files(
        config: Dict,
        file_names: List[Path]
) -> int:
    passed = True

    for file_name in file_names:
        logger.info(f"Processing {file_name}")
        module = extract_module(file_name=file_name)
        passed_ = check_dependencies(
            file_name=file_name,
            forbidden_imports=config.get(module, {}).get("forbidden_imports", [])
        )

        passed = passed_ and passed

    if passed:
        return 0

    return 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=False, default=None)
    parser.add_argument("file_names", nargs="*")
    args = parser.parse_args()

    path_config_file = args.config
    if path_config_file is None:
        path_config_file = Path(".import_check.toml")

    config = load(
        path_config_file=path_config_file
    )

    return check_all_files(
        config=config,
        file_names=[Path(f) for f in args.file_names]
    )


if __name__ == "__main__":
    raise SystemExit(main())
