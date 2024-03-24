"""
В этом файле будут Celery-задачи
"""
from typing import Generator, Any, Tuple, List, Optional

from celery.utils import log
from celery.exceptions import SoftTimeLimitExceeded
from celery.result import AsyncResult
from celery.schedules import crontab
from celery import shared_task
from werkzeug.datastructures import FileStorage

from .mail import send_email
from .image import blur_image
from . import celery_
from .requests_func_db import subscribe, get_emails_for_subscribe, del_email
from .utils_for_img import save_img, zip_img_before_send_email

logger = log.get_task_logger(__name__)


def process_images_blur(img_list: list[FileStorage], receiver: str) -> Optional[str]:
    """Принимает объекты FileStorage и сохраняет файлы для дальнейшей обработки."""
    save_img(files=img_list)

    filenames_collection: List[str] = list(file.filename for file in img_list)
    try:
        if img_list:
            result: AsyncResult = blur_endpoint_process.delay(img_list=filenames_collection, receiver=receiver)
            return result.id
        raise ValueError(f'Images list is empty {img_list=}')

    except SoftTimeLimitExceeded as err:
        logger.error(err)
    except ValueError as err:
        logger.error(err)


@celery_.task(soft_time_limit=60 * 5, time_limit=61 * 5, name='blur_endpoint_part_one')
def blur_endpoint_process(img_list: list[str], receiver: str) -> None:
    """Функция запускает задачи необходимые для отправки результатов на почту."""
    id_task = process_images_blur_and_save.delay(img_list=img_list)
    process_send_email(order_id=id_task.id, receiver=receiver, img_files=img_list)


def process_send_email(order_id: str, receiver: str, img_files: list[str]) -> None:
    """Формируется список имен файлов и запускается таска отправки сообщения."""
    img_files_blur = list(f'blur_{file}' for file in img_files)
    process_send_email_.delay(order_id=order_id, receiver=receiver, img_files=img_files_blur)


@shared_task(name='make_blur_img')
def process_images_blur_and_save(img_list: list[str], **_) -> None:
    """Обрабатывается список изображений."""
    [blur_image(src_filename=src_filename) for src_filename in img_list]


@celery_.task(name='make_zip_archive')
def zip_img(order_id: str, filenames: list[str]) -> None:
    """Архивируются изображения, которые были предварительно обработаны."""
    zip_img_before_send_email(order_id=order_id, filenames=filenames)


@shared_task(name='send_email')
def send_mail(order_id: str, receiver: str, filename: str) -> None:
    """Отправка email c zip архивом."""
    send_email(order_id=order_id, receiver=receiver, filename=filename)


@shared_task(name='run_processes_send_email_and_zip_img')
def process_send_email_(order_id: str, receiver: str, img_files: list[str]) -> None:
    """Запускает таску архивации изображений, а затем отправку email."""
    zip_img.delay(order_id=order_id, filenames=img_files)
    send_mail.delay(order_id=order_id, receiver=receiver, filename=order_id)


def subscribe_email(email: str, add_email: bool | None = None, unsubs_email: bool | None = None) -> None:
    if add_email:
        subscribe_send_emails.delay(email=email)
    elif unsubs_email:
        unsubscribe_send_emails.delay(email=email)
    else:
        raise ValueError(f"Params: add_email | del_email: Optional[str]")


@shared_task(name='unsubscribe_email')
def unsubscribe_send_emails(email: str) -> None:
    """
    Пользователь указывает почту и отписывается от рассылки.
    """
    del_email(email=email)


@shared_task(name='subscribe_email')
def subscribe_send_emails(email: str) -> None:
    """
    Пользователь указывает почту и подписывается на рассылку.
    Каждую неделю ему будет приходить письмо о сервисе на почту.
    """
    subscribe(email=email)


@shared_task(name='spam_emails_to_followers')
def send_emails_for_followers() -> None:
    """Рассылка сообщений по подписке на почту."""
    message = 'Сообщение на почту раз в семь дней по подписке'
    subscribes_collection = get_emails_for_subscribe()
    for email in subscribes_collection:
        logger.debug(f'{email.email}  was successful spent.')
        send_email(receiver=email.email, message=message)


@celery_.on_after_configure.connect
def setup_period_send_email(sender, **__) -> None:
    """
    Пользователь указывает почту и подписывается на рассылку.
    Каждую неделю ему будет приходить письмо о сервисе на почту.
     """
    try:
        sender.add_periodic_task(crontab(day_of_week='6'), send_emails_for_followers.s(),
                                 name='schedule_send_emails_to_followers'
                                 )
    except SoftTimeLimitExceeded as er:
        logger.error(f'<<{er}>>')


def get_status_task_by_order(order_id: str) -> Tuple[Any, str]:
    """
    Возвращает информацию о задаче: прогресс (количество обработанных задач)
    и статус (в процессе обработки, обработано, отправлено на почту).
    """
    children_task = 1
    total_task = 0
    completed_task = 0
    status_task: AsyncResult = celery_.AsyncResult(order_id)

    if status_task.state == 'FAILURE':
        return status_task.state, str(status_task.result)

    state: Generator[tuple[AsyncResult, Any | None], Any, None] = status_task.collect()

    for async_result_obj, _ in state:
        print('111')
        if async_result_obj.status == 'SUCCESS':
            completed_task += 1
        total_task += children_task

    return status_task.status, f'{completed_task}/{total_task}'
