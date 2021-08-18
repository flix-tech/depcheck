### Upgrade Python version

- Change the version constraint in `.python-version`
- Install the new version (either via `pyenv install` or manually)
- Change the version constraint in `pyproject.toml`
- Run `poetry lock --no-update` to recheck the `.lock` file, but not update any dependencies
- Run tests and check that everything looks fine
- Rebuild your virtual environment:
  - `rm -rf .venv` to remove Poetry's current virtual environment
  - `poetry install` to create the new environment
