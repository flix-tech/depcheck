import pprint
import sys

from depcheck.models import Ruleset, DependencyReport


class DepChecker:
    __ruleset: Ruleset
    __dependency_report: DependencyReport

    def __init__(self, ruleset: Ruleset,
                 dependency_report: DependencyReport) -> None:
        self.__ruleset = ruleset
        self.__dependency_report = dependency_report

    def run(self) -> None:
        # Check dependencies if there is any violation for given ruleset
        errors = {}
        for layer in self.__ruleset.rules:
            violations = self.__check_rule(layer)
            if len(violations) > 0:
                errors[layer] = violations

        if errors:
            print(f"There are {len(errors)} forbidden dependencies:")
            pprint.pprint(errors)
            sys.exit(1)
        else:
            print("OK")
            sys.exit(0)

    def __check_rule(self, layer: str) -> list[str]:
        violation: list[str] = []
        layer_deps: set[str] = self.__dependency_report.layer_dependencies(layer)
        whitelist: set[str] = self.__dependency_report.whitelist(layer)

        # Since some packages depend on the root package but the whitelist doesn't have
        # the root package explicitly, we need to add it to the whitelist.
        whitelist.add(self.__dependency_report.root_package)

        black_list = layer_deps.difference(whitelist)

        if len(black_list) > 0:
            violation.extend(list(black_list))

        return violation
