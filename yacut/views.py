from random import choices, randrange
import string

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import FileForm, URLMapForm
from .models import URLMap


def get_unique_short_id():
    """Формирует короткие идентификаторы переменной длины"""
    # Буквы + цифры
    characters = string.ascii_letters + string.digits
    while True:
        # Генерируем 6 случайных символов
        short_id = ''.join(choices(characters, k=6))
        # Проверяем в БД
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    short_link = None

    if form.validate_on_submit():
        custom_id = form.custom_id.data.strip() if form.custom_id.data else None
        if custom_id:
            # Проверка на занятость и на служебный адрес
            if custom_id == 'files' or URLMap.query.filter_by(short=custom_id).first():
                flash('Предложенный вариант короткой ссылки уже существует.')
                return render_template('index.html', form=form)
        else:
            # Если пользователь не ввел, генерируем
            custom_id = get_unique_short_id()
        urlmap = URLMap(
            original=form.original_link.data,
            short=custom_id
        )
        db.session.add(urlmap)
        db.session.commit()

        short_link = url_for('redirect_view', short_id=custom_id, _external=True)
        # пока непонятно куда будем редиректить
        # return redirect(url_for('opinion_view', id=opinion.id))
    return render_template('index.html', form=form, short_link=short_link)


@app.route('/<string:short_id>')
def redirect_view(short_id):
    """Перенаправляет на оригинальную ссылку"""
    urlmap = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(urlmap.original)


@app.route('/files')
def files_view():
    form = FileForm()
    short_links = None

    if form.validate_on_submit():
        custom_id = get_unique_short_id()
        # здесь будет загрузка на Ядиск:
        payload = {
            # Загрузить файл с названием filename.txt в папку приложения.
            'path': f'app:/filename.txt',  
            'overwrite': 'True'  # Если файл существует, перезаписать его.
        }
        response = requests.get(
            headers=AUTH_HEADERS,  # Заголовок для авторизации.
            params=payload,  # Указать параметры.
            url=REQUEST_UPLOAD_URL
        )
        upload_url = response.json()['href']
        with open('filename.txt', 'rb') as file:
            response = requests.put(
                data=file,
                url=upload_url,
            )

        # Расположение файла находится в заголовке Location.
        location = response.headers['Location']
        # Декодировать строку при помощи модуля urllib.
        location = urllib.parse.unquote(location)
        # Убрать первую часть расположения файла /disk, 
        # она не понадобится.
        location = location.replace('/disk', '')
        urlmap = URLMap(
            original=location,  # тут должна получиться ссылка на яндекс диск
            short=custom_id
        )
        db.session.add(urlmap)
        db.session.commit()
        # это наверное должен быть словарь типа имя файла: ссылка
        short_links = url_for('redirect_view', short_id=custom_id, _external=True)
    return render_template('add_files.html', form=form, short_links=short_links)
