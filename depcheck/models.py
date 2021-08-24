from typing import Any, Dict, List, Set

from depcheck.util import flatten


class Ruleset:
    __rules: Dict[str, List[str]]
    __layers: Dict[str, List[str]]

    def __init__(self, layers: Dict[str, List[str]], rules: Dict[str, List[str]]) -> None:
        self.__rules = rules
        self.__layers = layers

    def layer_packages(self, layer: str) -> List[str]:
        return self.layers.get(layer, [])

    def whitelist(self, layer: str) -> List[str]:
        return self.rules.get(layer, [])

    @property
    def rules(self) -> Dict[str, List[str]]:
        return self.__rules

    @property
    def layers(self) -> Dict[str, List[str]]:
        return self.__layers


class DependencyReport:
    __ruleset: Ruleset
    __graph: Dict[str, Any]
    __all_packages: List[str]

    def __init__(self, ruleset: Ruleset, dependency_graph: Dict[str, Any]) -> None:
        self.__ruleset = ruleset
        self.__graph = dependency_graph
        self.__all_packages = list(self.__graph.keys())

    def layer_dependencies(self, layer: str) -> Set[str]:
        layer_packages: Set[str] = self.__layer_packages([layer])
        layer_dependencies = self.__package_dependencies(layer_packages)

        return self.__exclude_inner_dependencies(layer_dependencies, layer_packages)

    def whitelist(self, layer: str) -> Set[str]:
        whitelist: List[str] = self.__ruleset.whitelist(layer)

        return self.__layer_packages(whitelist)

    @property
    def root_package(self) -> str:
        return self.__graph["__main__"]["imports"][0]

    @staticmethod
    def __exclude_inner_dependencies(raw_dependencies: Set[str], layers: Set[str]) -> Set[str]:
        return raw_dependencies - layers

    def __layer_packages(self, layers: List[str]) -> Set[str]:
        if layers is None:
            return set()

        # Packages within given layers
        layer_packages: List[str] = flatten([self.__ruleset.layer_packages(layer) for layer in layers])

        # Include subpackages of layer_packages
        layer_packages.extend(self.__subpackages(layer_packages))

        return set(layer_packages)

    def __subpackages(self, packages: List[str]) -> List[str]:
        subpackages: List[str] = []

        for package in self.__all_packages:
            if package.startswith(tuple(packages)):
                subpackages.append(package)

        return subpackages

    def __package_dependencies(self, packages: Set[str]) -> Set[str]:
        """
        Returns all packages that are used(imported) in given 'packages'.
        In other words, this returns dependencies of given 'packages'.
        """
        return set(flatten([self.__graph.get(i, {}).get("imports", []) for i in packages]))
