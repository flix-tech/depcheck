### Update project dependencies

- Change the version constraint in `pyproject.toml`. 
  e.g. update pydeps' version from "^1.9.13" to "^1.9.14"  
- Run tests and check that everything looks fine
- Rebuild your virtual environment:
  - `rm -rf .venv` to remove Poetry's current virtual environment
  - `poetry install` to create the new environment
