import argparse
import json
from copy import copy

from pydeps import target
from pydeps.py2depgraph import py2dep
from pydeps.pydeps import pydeps, externals


def print_arguments(arguments: list[str]):
    res = py2dep(
        target=target.Target("package_1"),
        # fname="package_1",
        show_raw_deps=True,
        format="svg",
        exclude_exact="",
        show_cycles=False,
        noise_level=2 ** 65,
        max_bacon=2 ** 65,
        show_deps=False,
        start_color=1,
        externals=True
    )

    rules = [{
        "package": "package_1",
        "forbidden_imports": ["package_2"],
        "levels": "all"
    }]

    for package, infos in res.sources.items():
        print(f"{package} <- {infos.imports} -> {infos.imported_by}")

        for rule in rules:
            # if levels == "all"
            if rule["package"] in package:
                for forbidden_import in rule["forbidden_imports"]:
                    # if levels == "all"
                    if forbidden_import in infos.imports:
                        raise ValueError(f"{forbidden_import} imported by {package}")

    # for argument in arguments:
    #     print(argument)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args()

    print_arguments(args.filenames)

    return 1


if __name__ == "__main__":
    exit(main())
