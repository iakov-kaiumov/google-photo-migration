import os
from pathlib import Path

from PIL import Image


def convert(filepath: Path) -> Path:
    image = Image.open(filepath).convert('RGB')
    output_filepath = filepath.parent / f'{filepath.stem}.jpg'
    image.save(output_filepath)
    os.remove(filepath)
    return output_filepath


if __name__ == '__main__':
    print((Path(__file__).resolve().parent / 'IMG_0669.PNG').stem)
