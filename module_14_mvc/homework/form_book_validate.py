from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired


class BookForm(FlaskForm):
    author_name = StringField(validators=[InputRequired(message="The author can't be empty"), ])
    book_title = StringField(validators=[InputRequired(message="The title can't be empty"), ])


class SearchAuthor(FlaskForm):
    search = StringField(validators=[InputRequired(message="It can't be empty"), ])
