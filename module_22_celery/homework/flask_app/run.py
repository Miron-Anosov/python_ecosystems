from python_advanced.module_22_celery.homework.flask_app import app

# /homework/flask_app/
#       celery -A app worker -B --loglevel=INFO | celery -A app flower --post=5555

if __name__ == '__main__':
    app.flask_.run()
