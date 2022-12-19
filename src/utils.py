from pathlib import Path


def get_folders_in_folder(directory: Path, prefix: str) -> list:
    dirs = []
    iterator = directory.iterdir()
    for x in iterator:
        if x.is_dir() and x.name.startswith(prefix):
            dirs.append(x)
    return dirs


def get_files_in_folder(directory: Path, prefix=None, suffix=None, recursively=False) -> list:
    files = []
    iterator = directory.rglob("*") if recursively else directory.iterdir()
    for x in iterator:
        if not x.is_file():
            continue
        if prefix and not x.name.startswith(prefix):
            continue
        if suffix and not x.name.endswith(suffix):
            continue
        files.append(x)
    return files


def test():
    base_dir = Path('/Users/iakov/Pictures/Takeout/Google Фото/').resolve()
    prefix = 'IMG_2058.jpg'
    print(get_files_in_folder(base_dir / 'Photos from 2021', prefix=prefix, suffix='json'))


if __name__ == '__main__':
    test()
