"""
В эндпоинт /registration добавьте все валидаторы, о которых говорилось в последнем видео:

1) email (текст, обязательно для заполнения, валидация формата);
2) phone (число, обязательно для заполнения, длина — десять символов, только положительные числа);
3) name (текст, обязательно для заполнения);
4) address (текст, обязательно для заполнения);
5) index (только числа, обязательно для заполнения);
6) comment (текст, необязательно для заполнения).
"""

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import InputRequired, Email, Length

from hw2_validators import number_length, NumberLength

app = Flask(__name__)


class RegistrationForm(FlaskForm):
    """Базовый класс для обработки пост запросов при регистрации."""
    email = StringField(
        validators=[InputRequired(message="The email can't be empty"), Email(message="The email doesn't correct")])

    phone = IntegerField(
        validators=[InputRequired(message="The phone can't be empty"),
                    number_length(min_value=1, max_value=999_999_99_99, message='The phone is invalid'),
                    NumberLength(min_len=10, max_len=10, message='The phone must be length only 10 numbers')])

    name = StringField(validators=[InputRequired(message="The name can't be empty")])

    address = StringField(validators=[InputRequired(message="The address can't be empty"),
                                      Length(min=3, max=100, message='The address is too short')])

    index = IntegerField(validators=[InputRequired(message="The index can't be empty"),
                                     NumberLength(min_len=5, max_len=6, message='The index length invalid')])
    comment = StringField()


@app.route("/registration", methods=["POST"])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        email, phone = form.email.data, form.phone.data

        return f"Successfully registered user {email} with phone +7{phone}"

    return f"Invalid input, {form.errors}", 400


if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
