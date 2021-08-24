# CONTRIBUTING

Start by searching through the [issues][issues] and
[pull requests][pull-requests] to see whether someone else has raised a similar idea or question. If you don't see your
idea listed, open a pull request.

## Maintenance Work

### Update project dependencies

- Change the version constraint in `pyproject.toml`. e.g. update pydeps' version from "^1.9.13" to "^1.9.14"
- Run tests and check that everything looks fine
- Rebuild your virtual environment:
    - `rm -rf path_to_env` to remove Poetry's current virtual environment
    - `poetry install` to create the new environment

<!-- Links -->
[issues]: https://github.com/flix-tech/depcheck/issues
[pull-requests]: https://github.com/flix-tech/depcheck/pulls
