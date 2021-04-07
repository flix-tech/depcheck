import json
from typing import Any

import yaml
from pytest import raises, fixture

from depcheck.depchecker import DepChecker
from depcheck.models import Ruleset, DependencyReport


@fixture()
def ruleset() -> Ruleset:
    """
    This is a simple ruleset which includes two layers which are layer_1 and layer_2.
    - Depended modules of each layer take place in the 'layers' part.
        e.g. layer_1 is depending on the 'root_package.package_1' module.
    - Dependencies between layers are configured in the 'whitelist' part. e.g:
        - 'layer_1: ~': layer_1 should not depend on any layers
        - 'layer_2: layer_1': layer_2 is allowed to depend on layer_1
    """
    config_yaml = '''
            layers:
              layer_1:
                - root_package.package_1
              layer_2:
              - root_package.package_2
            whitelist:
              layer_1: ~
              layer_2:
                - layer_1
    '''

    ruleset = yaml.safe_load(config_yaml)

    return Ruleset(layers=ruleset['layers'], rules=ruleset['whitelist'])


@fixture
def valid_dependencies() -> dict[str, Any]:
    """
    - 'root_package.package_1' module inside 'layer_1' doesn't import any modules.
    i.e. layer_1 doesn't depend on any layers.
    - 'root_package.package_2' module inside 'layer_2' depends on the 'root_package.package_1'
    module inside 'layer_1'. i.e. layer_2 depends on layer_1
    """
    return json.loads('''
                {
                    "__main__": {
                        "bacon": 0,
                        "imports": [
                            "root_package",
                            "root_package.__main__",
                            "root_package.package_1",
                            "root_package.package_1.model",
                            "root_package.package_2",
                            "root_package.package_2.usecase"
                        ],
                        "name": "__main__"
                    },
                    "root_package": {
                        "bacon": 1,
                        "imports": [
                            "root_package",
                            "root_package.package_1",
                            "root_package.package_2"
                        ],
                        "name": "root_package"
                    },
                    "root_package.__main__": {
                        "bacon": 1,
                        "name": "root_package.__main__"
                    },
                    "root_package.package_1": {
                        "bacon": 1,
                        "name": "root_package.package_1"
                    },
                    "root_package.package_1.model": {
                        "bacon": 1,
                        "name": "root_package.package_1.model"
                    },
                    "root_package.package_2": {
                        "bacon": 1,
                        "name": "root_package.package_2"
                    },
                    "root_package.package_2.usecase": {
                        "bacon": 1,
                        "imports": [
                            "root_package",
                            "root_package.package_1",
                            "root_package.package_1.model"
                        ],
                        "name": "root_package.package_2.usecase"
                    }
                }

        ''')


@fixture
def forbidden_dependencies() -> dict[str, Any]:
    """
        - 'root_package.package_1' module inside 'layer_1' depends on the 'root_package.package_2'
        module inside 'layer_2'. i.e. layer_1 depends on layer_2
        - 'root_package.package_2' module inside 'layer_2' depends on the 'root_package.package_1'
        module inside 'layer_1'. i.e. layer_2 depends on layer_1
        """
    return json.loads('''
                {
                    "__main__": {
                        "imports": [
                            "root_package",
                            "root_package.__main__",
                            "root_package.package_1",
                            "root_package.package_1.model",
                            "root_package.package_2",
                            "root_package.package_2.usecase"
                        ],
                        "name": "__main__"
                    },
                    "root_package": {
                        "imports": [
                            "root_package",
                            "root_package.package_1",
                            "root_package.package_2"
                        ],
                        "name": "root_package"
                    },
                    "root_package.package_1": {
                        "bacon": 1,
                        "name": "root_package.package_1"
                    },
                    "root_package.package_1.model": {
                        "bacon": 1,
                        "name": "root_package.package_1.model"
                    },
                    "root_package.package_2": {
                        "bacon": 1,
                        "name": "root_package.package_2"
                    },
                    "root_package.package_1.model": {
                        "imports": [
                            "root_package.package_2.usecase"
                        ],
                        "name": "root_package.package_1.model"
                    },
                    "root_package.package_2.usecase": {
                        "imports": [
                            "root_package",
                            "root_package.package_1",
                            "root_package.package_1.model"
                        ],
                        "name": "root_package.package_2.usecase"
                    }
                }
        ''')


def test_project_dependencies_are_valid(ruleset: Ruleset,
                                        valid_dependencies: dict[str, Any]) -> None:
    dependency_report: DependencyReport = DependencyReport(ruleset, valid_dependencies)

    with raises(SystemExit) as exception:
        DepChecker(ruleset, dependency_report).run()

    assert exception.type == SystemExit
    assert exception.value.code == 0


def test_project_dependencies_are_forbidden(ruleset: Ruleset,
                                            forbidden_dependencies: dict[str, Any]) -> None:
    dependency_report: DependencyReport = DependencyReport(ruleset, forbidden_dependencies)

    with raises(SystemExit) as exception:
        DepChecker(ruleset, dependency_report).run()

    assert exception.type == SystemExit
    assert exception.value.code == 1
