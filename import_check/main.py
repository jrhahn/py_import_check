import argparse
import logging
from pathlib import Path
from typing import List, Dict

from import_check.dependency import analyse


def reshape(rules: List[Dict]) -> Dict:
    return {
        rule.pop("module"): rule for rule in rules
    }


def process(
        file_names: List[Path],
        project_root: Path,
        rules: Dict,
) -> None:
    for file_name in file_names:
        this_module = str(file_name).split(str(project_root))[-1].split("/")[1]

        dependencies = analyse(Path(file_name))

        if this_module not in rules:
            print(f"No rule for {this_module} ({file_name})")
            continue

        forbidden_imports = rules[this_module]["forbidden_imports"]

        for d in dependencies:
            if d in forbidden_imports:
                raise ImportError(f"{file_name} should not import from {forbidden_imports}")

        print(file_name)
        print(f"\t{dependencies}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args()

    # process(args.filenames)
    this_module_root = "/home/jhahn/repositories/daprod-action-analytics-py/daproto-pose-similarity/"

    rules = [
        {
            "module": "daproto-pose-similarity",
            "forbidden_imports": ["daprod_dataset_tools"],
        }
    ]

    project_root = Path("/home/jhahn/repositories/daprod-action-analytics-py/")

    process(
        file_names=list(Path(this_module_root).rglob("*.py")),
        project_root=project_root,
        rules=reshape(rules=rules)
    )

    return 1


if __name__ == "__main__":
    exit(main())
