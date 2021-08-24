![Depcheck: Dependency Checker](https://images2.imgbox.com/da/85/J5OEzbAH_o.jpg)

Depcheck is a command line code-quality tool which supports adopting a 
layered architecture by making it possible to specify dependency constraints
between packages of your own Python application. 
The tool aims to achieve the same goals as [Deptrac][deptrac] in PHP and [JDepend][jdepend] in Java

## Install
Install from [Pypi][pypi-link] via `pip install depcheck`
    
## Usage
Let's say you have a project with the directory structure below:
```text
example
    root
        foo
        bar
        main.py
        __init__.py
    README.md
    .gitignore
    .depcheck.yml
```
Note: Package directories should contain **\_\_init\_\_.py** to be recognized as a package.
- Navigate to the `exampe` then run `depcheck` for your project:
    ```shell
    depcheck root
    ```
- As you can see in the directory structure above, we have `.depcheck.yml` 
  configuration file in the project directory. If you would like to change 
  the path of the configuration file, use `-f` or `--file` argument:
    ```shell
    depcheck root -f /path/to/your/custom/depcheck.yml
    ```

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
