from __future__ import annotations

import ast
from pathlib import Path

from import_check import LOG


def analyse(file: Path) -> set:
    modules = set()

    class ModuleLister(ast.NodeVisitor):
        def visit_Import(self, node):
            for name in node.names:
                modules.add(name.name.split(".")[0])

        def visit_ImportFrom(self, node):
            if node.module is not None and node.level == 0:
                modules.add(node.module.split(".")[0])

    node_iter = ModuleLister()

    with open(file) as fp:
        content = fp.read()

    try:
        parsed = ast.parse(content)
    except SyntaxError as e:
        LOG.error(e)
        return set()

    node_iter.visit(parsed)

    return modules
