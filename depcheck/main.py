from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from depcheck.depchecker import DepChecker
from depcheck.models import Ruleset, DependencyReport
from depcheck.readers import RulesetReader, DependencyReader

DEFAULT_CONFIG_FILE_PATH = ".depcheck.yml"


def main() -> None:
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    add_arguments(parser)
    args = parser.parse_args()

    print("# Reading ruleset...")
    ruleset: Ruleset = RulesetReader(args.file).read()
    print("# Reading project packages...")
    dependency_report: DependencyReport = DependencyReader(ruleset, args.root_package).read()
    print("# Checking dependencies...")
    DepChecker(ruleset, dependency_report).run()


def add_arguments(parser: ArgumentParser) -> None:
    parser.add_argument(
        "root_package",
        help="Root package of the project"
    )

    parser.add_argument(
        "-f",
        "--file",
        default=DEFAULT_CONFIG_FILE_PATH,
        help="Path to the config file that includes layers and rules.",
    )


if __name__ == "__main__":
    main()
