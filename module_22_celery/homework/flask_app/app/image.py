"""
Здесь происходит логика обработки изображения
"""
import os
from typing import Optional

from PIL import Image, ImageFilter


IMG_PATH = './img/'


def blur_image(src_filename: str, dst_filename: Optional[str] = None):
    """
    Функция принимает на вход имя входного и выходного файлов.
    Применяет размытие по Гауссу со значением 5.
    """
    abs_path_img = os.path.abspath(os.path.join('.', IMG_PATH))

    if not dst_filename:
        dst_filename = f'blur_{src_filename}'
    with Image.open(f'{abs_path_img}/{src_filename}') as img:
        img.load()
        new_img = img.filter(ImageFilter.GaussianBlur(5))
        new_img.save(f'{abs_path_img}/{dst_filename}')
