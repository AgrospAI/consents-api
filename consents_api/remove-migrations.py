import shutil
from pathlib import Path


def main() -> None:
    """
    Remove all migration directories from the project.
    """

    base_project_path = Path("project/")

    # Get all migration directories in the project
    migration_dirs = list(base_project_path.rglob("migrations"))

    # Remove the migrations directories
    for mdir in migration_dirs:
        if mdir.is_dir():
            print(f"Removing {mdir}")
            shutil.rmtree(mdir)


if __name__ == "__main__":
    main()
