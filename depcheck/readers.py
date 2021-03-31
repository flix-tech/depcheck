import json
import subprocess
from typing import Any

import yaml

from depcheck.models import Ruleset, DependencyReport


class RulesetReader:
    __filename: str

    def __init__(self, filename: str) -> None:
        self.__filename = filename

    def read(self) -> Ruleset:
        ruleset: dict[str, Any]

        with open(self.__filename, 'r') as stream:
            try:
                ruleset = yaml.safe_load(stream)
            except yaml.YAMLError:
                print('\n\n[!] Command must be run from project root '
                      'and .depcheck.yml file should be in the root\n\n')

        return Ruleset(layers=ruleset['layers'], rules=ruleset['whitelist'])


class DependencyReader:
    __ruleset: Ruleset
    __root_package: str

    def __init__(self, ruleset: Ruleset, root_package: str) -> None:
        self.__ruleset = ruleset
        self.__root_package = root_package

    def read(self) -> DependencyReport:
        output = subprocess.check_output("pydeps --show-deps --no-show --no-output --max-bacon 2 "
                                         + self.__root_package,
                                         shell=True).decode('u8').strip()
        dependency_graph: dict[str, Any] = json.loads(output)

        return DependencyReport(self.__ruleset, dependency_graph)
