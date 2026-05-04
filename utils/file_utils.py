from pathlib import Path


class PathNotFoundError(Exception):
    def __init__(self, path: Path) -> None:
        self.path = path
        super().__init__(f"Path not found: {path}")


class InvalidFileError(Exception):
    def __init__(self, path: Path) -> None:
        self.path = path
        super().__init__(f"Path is an invalid file: {path}")


def validate_file_path(path: Path) -> None:
    if not path.exists():
        raise PathNotFoundError(path)
    if not path.is_file():
        raise InvalidFileError(path)
