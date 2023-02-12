
import argparse
from pathlib import Path
from shutil import which
from subprocess import Popen
from datetime import datetime

parser = argparse.ArgumentParser(
            prog='autocommit',
            description='Will perform a git commit, then a git push',
         )

parser.add_argument("repo")
args = parser.parse_args()


def main(repo: str):
    if not which("git"):
        raise FileNotFoundError("Git executable not found in PATH")

    if not Path(repo).exists():
        raise FileNotFoundError(f"Repo {repo} not found")

    if not Path(repo).joinpath(".git").exists():
        raise FileNotFoundError(f"Repo {repo} is not initialized as a git repository")

    popen_args = ["git", "add", "."]
    print(f"Executing {' '.join(popen_args)}")
    Popen(popen_args, cwd=repo)

    commit_message = f"Autocommit message: timestamp {str(datetime.now())}"
    popen_args = ["git", "commit", "-a", "-m", f"'{commit_message}'"]
    print(f"Executing {' '.join(popen_args)}")
    Popen(popen_args, cwd=repo)

    popen_args = ["git", "push", "origin", "master"]
    print(f"Executing {' '.join(popen_args)}")
    Popen(popen_args, cwd=repo)


if __name__ == "__main__":
    main(repo=args.repo)
