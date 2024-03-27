from celery import Celery, Task
from flask import Flask

from .config import setting

__all__ = ['celery_', 'flask_']


def __create_celery_app(app: Flask) -> Celery:
    class FlassTask(Task):

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    app_celery_ = Celery(app.name, task_cls=FlassTask)
    app_celery_.config_from_object(setting.model_dump(include={"broker_url", 'result_backend'}))
    app_celery_.set_default()
    app.extensions['celery'] = app_celery_
    return app_celery_


flask_ = Flask(__name__, )

celery_ = __create_celery_app(flask_)

from .routes_app_flask import blur, status, subscribe, unsubscribe  # noqa
