import json
import logging
import os
from pathlib import Path
import datetime
from tqdm import tqdm

import png_to_jpg
from utils import get_files_in_folder, get_folders_in_folder
import date_setter

logging.basicConfig(
    format='\n\n%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

base_dir = Path('/Users/iakov/Pictures/Takeout/Google Фото/').resolve()
STR_MAX_LEN = 45

BAD_IMAGES_COUNT = 0

for subdir in get_folders_in_folder(base_dir, 'Photos from'):
    logger.info(f'Iterating subdir={subdir.name}')
    files = get_files_in_folder(subdir)
    files = list(filter(lambda x: x.suffix != '.json', files))

    for i in tqdm(range(len(files))):
        photo_filepath = files[i]

        prefix = photo_filepath.stem.split('-измененный')[0]
        prefix = prefix[0:min(len(prefix), STR_MAX_LEN)]
        jsons = get_files_in_folder(subdir, prefix=prefix, suffix='json')

        convert_json_file = False
        if photo_filepath.suffix.lower() == '.png':
            photo_filepath = png_to_jpg.convert(photo_filepath)
            convert_json_file = True

        if len(jsons) > 1:
            jsons = list(filter(lambda x: x.stem.split('.')[-1].lower() == photo_filepath.suffix[1:].lower(), jsons))
        if len(jsons) > 1:
            jsons = list(filter(lambda x: x.stem == photo_filepath.name, jsons))

        if len(jsons) == 1:
            json_filepath = jsons[0]

            with open(json_filepath, 'r') as json_file:
                data = json.load(json_file)
                timestamp = data['photoTakenTime']['timestamp']
                date = datetime.datetime.fromtimestamp(int(timestamp))

            if convert_json_file:
                new_name = '.'.join(json_filepath.stem.split('.')[0:-1]) + photo_filepath.suffix
                os.rename(json_filepath, json_filepath.parent / f'{new_name}.json')

            if photo_filepath.suffix.lower() == '.jpg':
                date_setter.set_date_for_jpg(photo_filepath, date)
            date_setter.set_anyfile_date(photo_filepath, date)
        elif len(jsons) == 0:
            logger.error(f'ERROR! Json not found {photo_filepath} prefix={prefix}')
            BAD_IMAGES_COUNT += 1
        else:
            logger.error(f'ERROR! To many jsons found \n{photo_filepath}\n{prefix}\n{jsons}\n\n')
            exit(-1)

logger.info(BAD_IMAGES_COUNT)
