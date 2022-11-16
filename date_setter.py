import logging
import datetime
from pathlib import Path

import piexif
from PIL import Image

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def set_date_for_jpg(photo_filepath: Path, date: str):
    try:
        _set_date_for_jpg(photo_filepath, date)
    except Exception as e:
        if str(e) == 'unpack requires a buffer of 2 bytes':
            Image.open(photo_filepath).convert('RGB').save(photo_filepath)
            _set_date_for_jpg(photo_filepath, date)
        else:
            logger.error(f'{e} {photo_filepath}')


def _set_date_for_jpg(photo_filepath: Path, date: str):
    filename = photo_filepath.__str__()

    exif_dict = piexif.load(filename)
    piexif.remove(filename)
    exif_dict['0th'][piexif.ImageIFD.DateTime] = date
    exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = date
    exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = date
    if piexif.ExifIFD.SceneType in exif_dict['Exif']:
        del exif_dict['Exif'][piexif.ExifIFD.SceneType]

    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, filename)


def test():
    date = datetime.datetime.now().strftime("%Y:%m:%d %H:%M:%S")
    filepath = Path(__file__).resolve().parent / 'IMG_20210503_205804.jpg'
    set_date_for_jpg(filepath, date)


if __name__ == '__main__':
    test()
