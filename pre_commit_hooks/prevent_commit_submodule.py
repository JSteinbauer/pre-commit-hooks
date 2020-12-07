import argparse
from typing import Optional
from typing import Sequence

from pre_commit_hooks.util import is_git_submodule


def _fix_file(
        filename: str,
        is_markdown: bool,
        chars: Optional[bytes],
) -> bool:
    with open(filename, mode='rb') as file_processed:
        lines = file_processed.readlines()
    newlines = [_process_line(line, is_markdown, chars) for line in lines]
    if newlines != lines:
        with open(filename, mode='wb') as file_processed:
            for line in newlines:
                file_processed.write(line)
        return True
    else:
        return False


def _process_line(
        line: bytes,
        is_markdown: bool,
        chars: Optional[bytes],
) -> bytes:
    if line[-2:] == b'\r\n':
        eol = b'\r\n'
        line = line[:-2]
    elif line[-1:] == b'\n':
        eol = b'\n'
        line = line[:-1]
    else:
        eol = b''
    # preserve trailing two-space for non-blank lines in markdown files
    if is_markdown and (not line.isspace()) and line.endswith(b'  '):
        return line[:-2].rstrip(chars) + b'  ' + eol
    return line.rstrip(chars) + eol


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    parser.add_argument(
        '--recursive',
        type=bool,
        default=False,
        help='Recursively search for .git folders in subordinate directories',
    )
    args = parser.parse_args(argv)
    if is_git_submodule(recursive=args.recursive):
        print('Repository is a submodule. To commit changes, pull edit '
              'and commit outside of the super repository')
        return 1
    else:
        print('OK')
        return 0


if __name__ == '__main__':
    exit(main())
