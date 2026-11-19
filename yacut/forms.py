from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from flask_wtf.file import FileAllowed, MultipleFileField
from wtforms.validators import DataRequired, Length


class MainForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 256)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, 256), DataRequired(message='Обязательное поле')]
    )
    submit = SubmitField('Добавить')


class FileForm(FlaskForm):
    files = MultipleFileField(
        validators=[
            FileAllowed(
                # Список разрешённых расширений для файлов.
                [],
                # Сообщение в случае, если расширение не совпадает.
                message=(
                    'Выберите файлы с расширением '
                    '???'
                )
            )
        ]
    )
    submit = SubmitField('Добавить')
