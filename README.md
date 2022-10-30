# *import-check* pre-commit hook

## Description
This pre-commit hook allows to prevent importing a Python module by another
Python module. In a configuration file for each module the list of *forbidden*
imports can be configured.

This is especially useful when working with a mono repository where there is only
a single virtual environment across all modules but you want to ensure that
importing internal modules follow certain conventions. One such convention could be
that certain modules should not imports others to prevent circular dependencies and
having the flexibility to package the modules separately in the future.

An alternative would be to test each module in its own virtual environment where
you have much better control over the packages that should be installed.
The downsides of the separate builds are that a) there might be mismatching requirements
between the modules and b) it obviously takes longer to set up isolated environments
which is critical in CI/CD.

## Configuration
Create a file named ``.import_check.toml`` in the root of the repository.
Note: Changing the location or the name of the configuration file is currently not supported.

The file should contain an entry for each module of your code. The name of a module is
given by the top level name in the folder structure.
Assuming you have a file structure like this:
```
|source
|- package_1
   |- code_1.py
|- package_2
   |- code_1.py
   |- code_2.py
```
Then ``package_1`` and ``package_2`` would be modules for which you could set up rules.

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
    rev: develop
    hooks:
    - id: import-check
```
and run ``pre-commit install``


## Update
To update the hook, simply run ``pre-commit autoupdate``.


## Limitations
- The configuration file must be located at the project root with the name
  ``.import_check.toml``
- Import checks can be configured only for modules at the top level, i.e. there is no support for submodules.
