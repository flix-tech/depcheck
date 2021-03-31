from typing import Any

from depcheck.util import flatten


class Ruleset:
    __rules: dict[str, list[str]]
    __layers: dict[str, list[str]]

    def __init__(self, layers: dict[str, list[str]],
                 rules: dict[str, list[str]]) -> None:
        self.__rules = rules
        self.__layers = layers

    def layer_packages(self, layer: str) -> list[str]:
        return self.layers.get(layer, [])

    def whitelist(self, layer: str) -> list[str]:
        return self.rules.get(layer, [])

    @property
    def rules(self) -> dict[str, list[str]]:
        return self.__rules

    @property
    def layers(self) -> dict[str, list[str]]:
        return self.__layers


class DependencyReport:
    __ruleset: Ruleset
    __graph: dict[str, Any]
    __all_packages: list[str]

    def __init__(self, ruleset: Ruleset,
                 dependency_graph: dict[str, Any]) -> None:
        self.__ruleset = ruleset
        self.__graph = dependency_graph
        self.__all_packages = list(self.__graph.keys())

    def layer_dependencies(self, layer: str) -> set[str]:
        layer_packages: set[str] = self.__layer_packages([layer])
        layer_dependencies = self.__package_dependencies(layer_packages)

        return self.__exclude_inner_dependencies(layer_dependencies, layer_packages)

    def whitelist(self, layer: str) -> set[str]:
        whitelist: list[str] = self.__ruleset.whitelist(layer)

        return self.__layer_packages(whitelist)

    @property
    def root_package(self) -> str:
        return self.__graph['__main__']['imports'][0]

    @staticmethod
    def __exclude_inner_dependencies(raw_dependencies: set[str], layers: set[str]) -> set[str]:
        return raw_dependencies - layers

    def __layer_packages(self, layers: list[str]) -> set[str]:
        if layers is None:
            return set()

        # Packages within given layers
        layer_packages: list[str] = flatten([self.__ruleset.layer_packages(layer)
                                             for layer in layers])

        # Include subpackages of layer_packages
        layer_packages.extend(self.__subpackages(layer_packages))

        return set(layer_packages)

    def __subpackages(self, packages: list[str]) -> list[str]:
        subpackages: list[str] = []

        for package in self.__all_packages:
            if package.startswith(tuple(packages)):
                subpackages.append(package)

        return subpackages

    def __package_dependencies(self, packages: set[str]) -> set[str]:
        """
        Returns all packages that are used(imported) in given 'packages'.
        In other words, this returns dependencies of given 'packages'.
        """
        return set(flatten([self.__graph.get(i, {}).get('imports', []) for i in packages]))
