import argparse
from typing import Optional
from typing import Sequence

from pre_commit_hooks.util import is_git_submodule


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    # the first argument will contain the file .pre-commit-config.yaml
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    # Optional flag to recursively search for .git folders in superordinate directories
    parser.add_argument(
        '--recursive',
        type=bool,
        default=False,
        help='Recursively search for .git folders in superordinate directories',
    )
    args = parser.parse_args(argv)
    if is_git_submodule(recursive=args.recursive):
        print('Repository is a submodule. To commit changes, pull edit '
              'and commit outside of the superordinate repository')
        return 1
    else:
        print('OK')
        return 0


if __name__ == '__main__':
    exit(main())
