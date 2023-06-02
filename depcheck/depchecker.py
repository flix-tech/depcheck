import sys
from typing import List, Set

from depcheck.models import DependencyReport, Ruleset


class DepChecker:
    __ruleset: Ruleset
    __dependency_report: DependencyReport

    def __init__(self, ruleset: Ruleset, dependency_report: DependencyReport) -> None:
        self.__ruleset = ruleset
        self.__dependency_report = dependency_report

    def run(self) -> None:
        # Check dependencies if there is any violation for given ruleset
        errors = {}

        for layer in self.__ruleset.rules:
            layer_defined_packages = self.__ruleset.layers[layer]
            detected_dependencies = self.__dependency_report.layer_dependencies(layer)

            print(f"\n### LAYER: '{layer}' WITH PACKAGES: {layer_defined_packages}")
            print(f"    DEPENDENCIES DETECTED:\n\t{detected_dependencies if detected_dependencies else 'none'}")

            violations = self.__check_rules(layer)
            if len(violations) > 0:
                errors[layer] = violations

        print("\n")

        if errors:
            print(f"!!! {len(errors)} ILLEGAL DEPENDENCIES FOUND:")
            packages_to_layers = self.__ruleset.packages_to_layers
            for layer, illegal_dependency_pkg in errors.items():
                for dependency in illegal_dependency_pkg:
                    illegal_layer_name = "?"
                    if dependency in packages_to_layers:
                        illegal_layer_name = packages_to_layers[dependency]
                    print(f"- Layer '{layer}' depends on '{dependency}' (Layer: {illegal_layer_name})")
            sys.exit(1)
        else:
            print("OK! All package dependencies look good!")
            sys.exit(0)

    def __check_rules(self, layer: str) -> List[str]:
        violation: List[str] = []
        layer_deps: Set[str] = self.__dependency_report.layer_dependencies(layer)
        whitelist: Set[str] = self.__dependency_report.whitelist(layer)

        black_list = layer_deps.difference(whitelist)

        if len(black_list) > 0:
            violation.extend(list(black_list))

        return violation
