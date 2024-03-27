import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .config import setting

SMTP_HOST, SMTP_PORT, SMTP_PASSWORD, SMTP_USER = (setting.smtp_host,
                                                  setting.smtp_port, setting.smtp_password, setting.smtp_user)

IMG_PATH = '../img/'


def send_email(receiver: str, order_id: str | None = None, filename: str | None = None, message: str | None = None):
    """
    Отправляет пользователю `receiver` письмо по заказу `order_id` с приложенным файлом `filename`

    Вы можете изменить логику работы данной функции
    """
    abs_path_img = os.path.abspath(os.path.join('flask_app', IMG_PATH))
    path_file = f'{abs_path_img}/{filename}.zip'

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)

        email = MIMEMultipart()
        email['Subject'] = f'Изображения. Заказ №{order_id}' if filename else 'Рассылка спама'
        email['From'] = SMTP_USER
        email['To'] = receiver

        if filename:
            with open(path_file, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())

            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={order_id}.zip'
            )
            email.attach(part)
        else:
            email.attach(MIMEText(message, 'plain'))

        text = email.as_string()

        server.sendmail(SMTP_USER, receiver, text)
