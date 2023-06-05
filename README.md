![Depcheck: Dependency Checker](https://images2.imgbox.com/da/85/J5OEzbAH_o.jpg)

Depcheck is a command line code-quality tool which supports adopting a layered architecture
by making it possible to specify dependency constraints between packages of your own Python application.
The tool aims to achieve the same goals as [Deptrac][deptrac] in PHP and [JDepend][jdepend] in Java

## Install
- Via [`poetry`][poetry] (recommended): Install with `poetry add depcheck`
- Via `pip`: Install from [Pypi][pypi-link] via `pip install depcheck`

## Usage
To run via CLI you run:
```shell
depcheck <root_dir> -f <config_file>

# Or, with poetry
poetry run depcheck <root_dir> -f <config_file>
```

The `example` directory demonstrates how the tool works.

```shell
cd example

poetry run depcheck example -f .depcheck.ok.yml  # This should be correct
poetry run depcheck example -f .depcheck.errors.yml  # This should give errors
```

To understand how to configure the tool, look inside the YML files. The `-f` argument is optional.
Implicitly, the tool will look for `.depcheck.yml`.

**NOTE:** Package directories should contain `__init__.py` to be recognized as a package!


## Contributing
All contributions are welcomed! See our [CONTRIBUTING.md][contribution] document.


<!-- Links -->
[hexagonal-architecture]: https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)
[upgrade-python-version]: ./docs/upgrade-python-version.md
[update-project-dependencies]: ./docs/upgrade-python-version.md
[pypi-link]: https://pypi.org/project/depcheck/
[contribution]: ./CONTRIBUTING.md
[deptrac]: https://github.com/qossmic/deptrac
[jdepend]: https://github.com/clarkware/jdepend
[poetry]: https://python-poetry.org/
