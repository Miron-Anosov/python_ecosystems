"""Здесь сохраняются изображения и архивируются перед отправкой."""

import zipfile
import os

from werkzeug.datastructures import FileStorage
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

IMG_PATH = './img/'

abs_path_img = os.path.abspath(os.path.join('.', IMG_PATH))


def save_img(files: list[FileStorage]) -> None:
    for file in files:
        with open(file=f'{abs_path_img}/{file.filename}', mode='wb') as img:
            img.write(file.stream.read())


def zip_img_before_send_email(filenames: list, order_id: str) -> None:
    with zipfile.ZipFile(file=f'{abs_path_img}/{order_id}.zip', mode='w') as z_file:
        for f, d, files in os.walk(abs_path_img):
            for file_blur_img in files:
                if file_blur_img in filenames:
                    logger.debug(f'{abs_path_img}/{file_blur_img}')
                    z_file.writestr(zinfo_or_arcname=file_blur_img, data=f'{abs_path_img}/{file_blur_img}')


def del_zip_img_after_send_email(): ...
