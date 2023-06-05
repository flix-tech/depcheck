import sys
from copy import copy
from importlib import import_module
from typing import Any, cast

from depcheck.util import flatten


class Ruleset:
    __rules: dict[str, list[str]]
    __layers: dict[str, list[str]]

    def __init__(self, layers: dict[str, list[str]], rules: dict[str, list[str]]) -> None:
        self.__validate_layers(layers)
        self.__layers = layers
        self.__rules = rules

    @staticmethod
    def __validate_layers(layers: dict[str, list[str]]) -> None:
        for packages in layers.values():
            for package in packages:
                try:
                    import_module(package)
                except ModuleNotFoundError:
                    print(f"\tERROR: There is no package or module named '{package}'!")
                    sys.exit(1)

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

    @property
    def packages_to_layers(self) -> dict[str, str]:
        out = {}
        for layer_name, packages_list in self.__layers.items():
            for package in packages_list:
                if package in out:
                    raise Exception(f"Package {package} is already in layer {out[package]}")
                out[package] = layer_name
        return out

    def packages_in_same_layer(self, layer: str, parent_package: str, detected_package: str) -> bool:
        if len(detected_package) < len(parent_package):
            # A package cannot be child of another package if the latter has shorter name
            return False

        if not detected_package.startswith(parent_package):
            return False

        pkg_to_layers = self.packages_to_layers
        if detected_package in pkg_to_layers and pkg_to_layers[detected_package] != layer:
            return False

        return True


class DependencyReport:
    __ruleset: Ruleset
    __graph: dict[str, Any]

    def __init__(self, ruleset: Ruleset, dependency_graph: dict[str, Any]) -> None:
        self.__ruleset = ruleset
        self.__graph = dependency_graph

    def layer_dependencies(self, layer: str) -> set[str]:
        # layer packages including subpackages detected
        layer_packages: set[str] = self.__layer_packages([layer])
        layer_dependencies = self.__package_dependencies(layer_packages)

        dependencies = self.__exclude_inner_dependencies(layer_dependencies, layer_packages)
        files = set()
        for dep in dependencies:
            maybe_module = import_module(dep)
            if not maybe_module:
                continue

            file_name = cast(str, maybe_module.__file__)
            if "__init__.py" not in file_name:
                files.add(dep)

        # Remove individual files and the root package
        return dependencies.difference(files.union({self.root_package}))

    def whitelist(self, layer: str) -> set[str]:
        whitelist: list[str] = self.__ruleset.whitelist(layer)

        return self.__layer_packages(whitelist)

    @property
    def root_package(self) -> str:
        if "__main__" not in self.__graph:
            print("\tERROR: Please make sure your root package has the `__init__.py` file and retry!")
            sys.exit(1)

        return self.__graph["__main__"]["imports"][0]

    @staticmethod
    def __exclude_inner_dependencies(raw_dependencies: set[str], layers: set[str]) -> set[str]:
        return raw_dependencies - layers

    def __layer_packages(self, layers: list[str]) -> set[str]:
        if layers is None:
            return set()

        # Packages within given layers
        layer_packages: list[str] = flatten([self.__ruleset.layer_packages(layer) for layer in layers])

        # Include subpackages of layer_packages
        for layer in layers:
            layer_packages.extend(self.__subpackages(layer, layer_packages))

        return set(layer_packages)

    def __subpackages(self, layer: str, parent_packages: list[str]) -> list[str]:
        subpackages: set[str] = set()

        detected_packages = list(self.__graph.keys())

        for parent_package in parent_packages:
            for detected_package in detected_packages:
                if self.__ruleset.packages_in_same_layer(layer, parent_package, detected_package):
                    subpackages.add(detected_package)

        pkg_to_layers = self.__ruleset.packages_to_layers

        subp_copy = copy(subpackages)
        for idx, sp in enumerate(subp_copy):
            for pkg, pkg_layer in pkg_to_layers.items():
                if sp.startswith(pkg) and pkg_layer != layer and sp in subpackages:
                    # Remove the subpackages that belong in different layers
                    # eg: if we have layer 1="a" and layer 2="a.b", then "a.b.c" does not belong in layer 1
                    subpackages.remove(sp)

        return list(subpackages)

    def __package_dependencies(self, packages: set[str]) -> set[str]:
        """
        Returns all packages that are used(imported) in given 'packages'.
        In other words, this returns dependencies of given 'packages'.
        """
        deps = set(flatten([self.__graph.get(i, {}).get("imports", []) for i in packages]))
        return set([item for item in deps if item not in packages])
