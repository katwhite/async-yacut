from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from flask_wtf.file import FileAllowed, MultipleFileField
from wtforms.validators import DataRequired, Length, Optional


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 256)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Optional(),
                    Length(1, 16,
                           message='Длина не должна превышать 16 символов')]
    )
    submit = SubmitField('Создать')


class FileForm(FlaskForm):
    files = MultipleFileField()
    submit = SubmitField('Загрузить')
