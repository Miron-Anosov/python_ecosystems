"""
В этом файле будет ваше Flask-приложение
"""

from flask import request, jsonify

from . import flask_
from .tasks import process_images_blur, get_status_task_by_order, subscribe_email


@flask_.route('/blur/', methods=['POST', ])
def blur():
    """Ставит в очередь обработку переданных изображений. Возвращает ID задачи."""
    email_address = request.form.get('email')
    images = request.files.getlist('files')
    if email_address:

        id_order = process_images_blur(img_list=images, receiver=email_address)

        if id_order:
            return jsonify({'id order': id_order}), 202
        return jsonify()

    return jsonify(f'email  is invalid. email={email_address}')


@flask_.route('/status/', methods=['GET', ])
def status():
    """
    Возвращает информацию о задаче: прогресс (количество обработанных задач)
    и статус (в процессе обработки, обработано, отправлено на почту).
    """
    order = request.args.get('order')
    status_task, progress = get_status_task_by_order(order_id=order)
    return jsonify({'status': status_task, 'progress': progress}), 200


@flask_.route('/subscribe/', methods=["POST", ])
def subscribe():
    """
    Пользователь указывает почту и подписывается на рассылку.
    Каждую неделю ему будет приходить письмо о сервисе на почту
    """
    email_address: dict = request.json

    if email := email_address.get('email'):
        subscribe_email(email=email, add_email=True)
        return jsonify({'successful': "email_address is subscribed"}), 202

    return jsonify({'failure': 'error: empty form'}), 412


@flask_.route('/unsubscribe/', methods=['POST', ])
def unsubscribe():
    """Пользователь указывает почту и отписывается от рассылки."""
    email_address = request.json

    if email := email_address.get('email'):
        subscribe_email(email=email, unsubs_email=True)
        return jsonify({'successful': "email_address is unsubscribed"}), 202

    return jsonify({'failure': 'error: empty form'}), 412
