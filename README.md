# py_import_check

## Description

## Configuration
Create a file named ``.import_check.toml`` in the root of the repository.
Note: currently it is not supported to change the location or the name of
the configuration file.

The file should contain an entry for each module in your code. A module is
defined by the top level name in code.
Assuming you have a file structure like
```
| source
|- package_1
   |- code_1.py
|- package_2
   |- code_1.py
   |- code_2.py
```
then ``package_1`` and ``package`` would be modules for which you could set up rules.

An example configuration for the file structure above where we want to make sure that
no single file inside ``package_2`` imports from ``package_1`` would be:
```toml
[package_2]
forbidden_imports = [ "package_1" ]
```

## Installation
In order to execute import-check before committing your code changes, add the following
lines to the project's ``.pre-commit-config.yaml``:
```yaml
-   repo: git@github.com:jrhahn/py_import_check.git
    rev: b60c093e93dad43ddf10feede8fdc0eac231371a
    hooks:
    - id: import-check
```
and run ``pre-commit install``


## Update
To update the hook, simply run ``pre-commit autoupdate``.
