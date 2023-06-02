from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

from depcheck.depchecker import DepChecker
from depcheck.models import DependencyReport, Ruleset
from depcheck.readers import DependencyReader, RulesetReader

DEFAULT_CONFIG_FILE_PATH = ".depcheck.yml"


def run_depcheck() -> None:
    command_args = create_argument_parser().parse_args()
    arg_config_file = command_args.file
    arg_root_package = command_args.root_package

    print(f"** Reading ruleset from '{arg_config_file}'")
    ruleset: Ruleset = RulesetReader(arg_config_file).read()
    print(f"** Reading project packages from root package: '{arg_root_package}'")
    dependency_report: DependencyReport = DependencyReader(ruleset, arg_root_package).read()
    print("** Checking dependencies")
    DepChecker(ruleset, dependency_report).run()


def create_argument_parser() -> ArgumentParser:
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument("root_package", help="Root package of the project")
    parser.add_argument(
        "-f",
        "--file",
        default=DEFAULT_CONFIG_FILE_PATH,
        help="Path to the config file that includes layers and rules.",
    )

    return parser


run_depcheck() if __name__ == "__main__" else None
