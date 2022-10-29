from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Sequence

from import_check.dependency import analyse
from import_check.import_check_configuration import load

logger = logging.getLogger(__name__)


def extract_module(file_name: Path) -> str:
    return file_name.parts[0]


def check_dependencies(
    file_name: Path,
    forbidden_imports: list[str],
) -> bool:
    passed = True

    logger.info(f"Checking {file_name}..")
    dependencies = analyse(file=file_name)

    for d in dependencies:
        passed_ = d not in forbidden_imports

        if not passed_:
            logger.info(
                f"{file_name} should not import from {forbidden_imports}"
            )

        passed = passed_ and passed

    return passed


def check_all_files(config: dict, file_names: list[Path]) -> int:
    passed = True

    for file_name in file_names:
        logger.info(f"Processing {file_name}")
        module = extract_module(file_name=file_name)
        passed_ = check_dependencies(
            file_name=file_name,
            forbidden_imports=config.get(module, {}).get(
                "forbidden_imports", []
            ),
        )

        passed = passed_ and passed

    if passed:
        return 0

    return 1


def parse_args(args: Sequence[str] | None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=False, default=None)
    parser.add_argument("file_names", nargs="*")
    return parser.parse_args(args=args)


def main(args: Sequence[str] | None = None) -> int:
    parsed_args = parse_args(args=args)
    path_config_file = parsed_args.config

    if path_config_file is None:
        path_config_file = Path(".import_check.toml")

    config = load(path_config_file=path_config_file)

    return check_all_files(
        config=config, file_names=[Path(f) for f in parsed_args.file_names]
    )


if __name__ == "__main__":
    raise SystemExit(main(args=sys.argv[1:]))
