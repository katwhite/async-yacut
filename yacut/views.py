import asyncio
import os
from random import choices
import string

import aiohttp
from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import FileForm, URLMapForm
from .models import URLMap


async def upload_file_to_yandex_disk(file, session):
    """Загружает файл на ЯДиск и возвращает прямую ссылку на скачивание"""
    # Уникальное имя для файла на диске, чтобы не перезаписывать чужие файлы
    disk_filename = f"{os.urandom(8).hex()}_{file.filename}"
    disk_path = f"app:/{disk_filename}"
    headers = app.config['AUTH_HEADERS']

    # 1. Запрос URL для загрузки файла
    upload_url = app.config['REQUEST_UPLOAD_URL']
    params = {'path': disk_path, 'overwrite': 'True'}

    async with session.get(upload_url, headers=headers, params=params) as response:
        response.raise_for_status()
        data = await response.json()
        upload_href = data['href']

    # 2. Загрузка файла по полученному URL
    async with session.put(upload_href, data=file.read()) as response:
        response.raise_for_status()

    # 3. Получение ссылки на скачивание (строго по инструкции)
    download_url = f"{app.config['API_HOST']}{app.config['API_VERSION']}/disk/resources/download"
    async with session.get(
        download_url, 
        headers=headers, 
        params={'path': disk_path}
    ) as response:
        response.raise_for_status()
        data = await response.json()
        return data['href']  # Возвращаем прямую ссылку на скачивание


async def async_upload_files(files):
    """Асинхронно загружает список файлов и возвращает список ссылок"""
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = [upload_file_to_yandex_disk(file, session) for file in files]
        results = await asyncio.gather(*tasks)
    return results


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


@app.route('/files', methods=['GET', 'POST'])
def files_view():
    form = FileForm()
    short_links = []

    if form.validate_on_submit():
        files = form.files.data
        try:
            # Получаем список прямых ссылок на скачивание
            yandex_download_urls = asyncio.run(async_upload_files(files))

            for file, download_url in zip(files, yandex_download_urls):
                short_id = get_unique_short_id()

                urlmap = URLMap(
                    original=download_url,
                    short=short_id
                )
                db.session.add(urlmap)
                short_links.append((
                    file.filename,
                    url_for('redirect_view', short_id=short_id, _external=True)
                ))
            db.session.commit()
        except Exception as e:
            flash(f'Ошибка при загрузке на Яндекс.Диск: {e}')
            db.session.rollback()
            return render_template('add_files.html', form=form)
    return render_template('add_files.html', form=form, short_links=short_links)
