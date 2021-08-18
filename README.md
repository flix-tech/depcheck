![Depcheck: Dependency Checker](/docs/.img/depcheck_logo.jpg)

Depcheck is a tool to check package-dependencies between predefined layers. 
In the configuration file(`.depcheck.yml`) located in the project root, 
which packages belong to which layers and allowed dependencies between 
layers are configurable. In this way, you can make sure that the application 
always complies with the [Hexagonal Architecture][hexagonal-architecture] 
principle of creating loosely coupled application components.

## Install
Install from [Pypi][pypi-link] via `pip install depcheck`
    
## Usage
Let's say you have a project with the directory structure below:
```text
project_directory
    root_package
        package-1
        package-2
        main.py
    README.md
    .gitignore
    .depcheck.yml
```
- Navigate to the `project_directory` then run `depcheck` for your project:
    ```shell
    depcheck root_package
    ```
- As you can see in the directory structure above, we have `.depcheck.yml` 
  configuration file in the project directory. If you would like to change 
  the path of the configuration file, use `-f` or `--file` argument:
    ```shell
    depcheck root_package -f config/customized_depcheck.yml
    ```

## Contributing
All contributions are welcomed! Start by searching through the [issues][issues] and 
[pull requests][pull-requests] to see whether someone else has raised a similar idea or question.
If you don't see your idea listed, open a pull request.

## Maintenance Work
- [Upgrade project's Python version][upgrade-python-version]
- [Update project dependencies][update-project-dependencies]


<!-- Links -->
[hexagonal-architecture]: https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)
[upgrade-python-version]: ./docs/upgrade-python-version.md
[update-project-dependencies]: ./docs/upgrade-python-version.md
[pypi-link]: https://pypi.org/project/depcheck/
[issues]: https://github.com/flix-tech/depcheck/issues
[pull-requests]: https://github.com/flix-tech/depcheck/pulls
