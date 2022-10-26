import argparse
from pathlib import Path
from typing import List

from import_check.dependency import analyse


def process(file_names: List[Path]):
    rules = {
        "daproto-pose-similarity": {
            "forbidden_imports": ["daprod_dataset_tools"],
            "levels": "all"
        }
    }

    project_root = "/home/jhahn/repositories/daprod-action-analytics-py/"

    for file_name in file_names:
        this_module = str(file_name).split(project_root)[-1].split("/")[0]

        dependencies = analyse(Path(file_name))

        forbidden_imports = rules[this_module]["forbidden_imports"]

        for d in dependencies:
            if d in forbidden_imports:
                raise ImportError(f"{file_name} should not import from {forbidden_imports}")

        print(file_name)
        print(f"  {dependencies}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args()

    # process(args.filenames)
    root = "/home/jhahn/repositories/daprod-action-analytics-py/daproto-pose-similarity/"

    process(list(Path(root).rglob("*.py")))
    return 1


if __name__ == "__main__":
    exit(main())
