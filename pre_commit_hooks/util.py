import os
import subprocess
from typing import Any
from typing import List
from typing import Optional
from typing import Set


class CalledProcessError(RuntimeError):
    pass


def added_files() -> Set[str]:
    cmd = ('git', 'diff', '--staged', '--name-only', '--diff-filter=A')
    return set(cmd_output(*cmd).splitlines())


def cmd_output(*cmd: str, retcode: Optional[int] = 0, **kwargs: Any) -> str:
    kwargs.setdefault('stdout', subprocess.PIPE)
    kwargs.setdefault('stderr', subprocess.PIPE)
    proc = subprocess.Popen(cmd, **kwargs)
    stdout, stderr = proc.communicate()
    stdout = stdout.decode()
    if retcode is not None and proc.returncode != retcode:
        raise CalledProcessError(cmd, retcode, proc.returncode, stdout, stderr)
    return stdout

def is_git_submodule(recursive: bool = False) -> bool:
    """Checks if the current directory is a git submodule
    Args:
        recursive (bool): If true, checks all superdirectories up to the (but
        not including) the home folder for .git files. Example: If the current
        directory is

            /home/usr/ondewo/ondewo-repo/ondewo-sub-module/

        it will check all directories

            home/usr/ondewo/ondewo-repo/, home/usr/ondewo/

        for .git folders.
    Returns:
    """

    cwd = os.getcwd()

    # Check that current working directory is a git repository
    if not os.path.exists(os.path.join(cwd, '.git')):
        raise FileNotFoundError(
            'No ".git" folder found in the current working directory. '
            'Not a git repository!')

    # Check if the superordinate folder is a git repo
    super_dir = '/'.join(cwd.split('/')[:-1])
    is_submodule = os.path.exists(os.path.join(super_dir, '.git'))

    if not is_submodule and recursive:
        super_dir = '/'.join(super_dir.split('/')[:-1])
        homedir = os.path.expanduser('~')
        while super_dir != homedir:
            if len(super_dir) <= len(homedir):
                raise RecursionError(
                    'Recursively checking the subordinate directories failed.')
            is_submodule = is_submodule or os.path.exists(
                os.path.join(super_dir, '.git'))

            # .git folder is found break the loop, else continue recursion
            if is_submodule:
                break
            else:
                super_dir = '/'.join(super_dir.split('/')[:-1])

    return is_submodule


def zsplit(s: str) -> List[str]:
    s = s.strip('\0')
    if s:
        return s.split('\0')
    else:
        return []
