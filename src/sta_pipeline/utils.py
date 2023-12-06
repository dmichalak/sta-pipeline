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
    """Creates a file in the directory to indicate job success."""
    directory = Path(directory).absolute()
    with open(directory / f"{job_name}.success", "w"):
        pass


def check_job_success(
    directory: Path,
):
    """Checks if a job has been run successfully."""
    directory = Path(directory).absolute()
    return directory.glob("*.success")       