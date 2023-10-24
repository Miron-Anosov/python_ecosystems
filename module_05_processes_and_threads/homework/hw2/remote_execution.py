"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""
import html
import subprocess
from typing import List

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired

app = Flask(__name__)


class CodeForm(FlaskForm):
    """
    Клас принимает параметры и проверяет их валидность.
    Attributes:
        code: код для обработки субпроцессом.
        timeout: время на выполнения кода.
    """
    code = StringField(validators=[InputRequired()])
    timeout = IntegerField(validators=[InputRequired()])


def run_python_code_in_subproccess(code: str, timeout: int) -> str:
    """
    Функция обрабатывает команду субпроцесса и возвращает строковое значение.
    Args:
        code: str: строка кода.
        timeout: int:  таймер.
    """
    cmd: List[str] = ['prlimit', '--nproc=1:1', 'python3', '-c', code]
    with subprocess.Popen(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as code_py:
        try:
            stdout, stderr = code_py.communicate(timeout=timeout)
            response_py_code: str = ''.join(stdout + stderr)
        except subprocess.TimeoutExpired:
            code_py.kill()
            response_py_code: str = 'Timeout'
        return response_py_code


@app.route('/run_code', methods=['POST'])
def run_code():
    """
    Проверяет валидность форм, передает их в функцию для обработки команды и возвращает от нее ответ.
    """
    form = CodeForm()
    if form.validate_on_submit():
        code, timeout = form.code.data, form.timeout.data
        output_code: str = run_python_code_in_subproccess(code=code, timeout=timeout)
        response: str = html.escape(output_code)
        return f'<pre>{response}</pre>'
    return f"Invalid input, {form.errors}", 400


if __name__ == '__main__':
    app.config['WTF_CSRF_ENABLED'] = False
    app.run(debug=True)
