import os
from pathlib import Path
from contextlib import contextmanager

@contextmanager
def cd(path):
    """Changes working directory and returns to previous on exit."""
    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)

    return

def job_success(
    directory: Path,
    job_name: str,
    ) -> None:

    directory = Path(directory).absolute()
    with open(directory / f"{job_name}.success"):
        pass

def check_job_success(
    directory: Path,
    ) -> list:

    extension = ".success"
    directory = Path(directory).absolute()

    files = [file.name for file in directory.glob(f"*{extension}")]
    return files