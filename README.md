![Depcheck: Dependency Checker](/docs/.img/depcheck_logo.jpg)

[![pipeline status](https://git.flix.tech/network/optimization/depcheck/badges/master/pipeline.svg)](https://git.flix.tech/network/optimization/depcheck/-/commits/master)

Depcheck is a tool to check package-dependencies between predefined layers. In the configuration file(`.depcheck.yml`) located in the project root, which packages belong to which layers and allowed dependencies between layers are configurable. In this way, you can make sure that the application always complies with the <a href="https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)">Hexagonal Architecture</a> principle of creating loosely coupled application components.

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
- As you can see in the directory structure above, we have `.depcheck.yml` configuration file in the project directory. If you would like to change the path of the configuration file, use `-f` or `--file` argument:
    ```shell
    depcheck root_package -f config/customized_depcheck.yml
    ```
