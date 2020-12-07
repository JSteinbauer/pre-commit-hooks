from typing import Tuple

import pytest
import os
import shutil

from pre_commit_hooks.prevent_commit_submodule import main as prevent_commit_submodule_main


class TestPreventCommitSubmodules:
    cwd = os.getcwd()
    path1 = os.path.join(cwd, 'tmp')
    path2 = os.path.join(path1, 'subdir1')
    path3 = os.path.join(path2, 'subdir2')
    path4 = os.path.join(path3, 'subdir3')

    @pytest.fixture(scope="function")
    def tmp_directories(self) -> Tuple[str]:
        """ create test directory with complex subdirectory structure
            - tmp
                .git
                - subdir1
                    .git
                    - subdir2
                        - subdir3
                            .git

        """
        os.mkdir(self.path1)

        os.mkdir(self.path2)
        os.mkdir(os.path.join(self.path1, '.git'))
        os.mkdir(self.path3)
        os.mkdir(os.path.join(self.path2, '.git'))
        os.mkdir(self.path4)
        os.mkdir(os.path.join(self.path4, '.git'))

        yield

        # Remove testing directories
        shutil.rmtree(self.path1)

    @pytest.mark.parametrize('working_dir,is_repo,is_submodule,recursive', [
        (path2, True, 1, False),
        (path3, False, 0, False),
        (path4, True, 0, False),
    ])
    def test_prevent_commit_submodule(
            self,
            tmp_directories: Tuple[str],
            working_dir: str,
            is_repo: bool,
            is_submodule: int,
            recursive: bool,
    ) -> None:
        os.chdir(working_dir)
        try:
            testreturn = prevent_commit_submodule_main()
        except FileNotFoundError:
            assert not is_repo
        else:
            assert testreturn == is_submodule