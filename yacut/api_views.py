from http import HTTPStatus
import re
from flask import jsonify, request

from yacut.constants import MAX_LENGTH_SHORT, SHORT_ID_PATTERN
from .error_handlers import InvalidAPIUsage
from . import app, db
from .models import URLMap


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    urlmap = URLMap.query.filter_by(short=short_id.strip()).first()
    if not urlmap:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': urlmap.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_url():
    data = request.get_json(force=True, silent=True)
    if not data or not isinstance(data, dict):
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    original_url = data['url']
    if not isinstance(original_url, str):
        raise InvalidAPIUsage('"url" является обязательным полем!')
    original_url = original_url.strip()

    custom_id = data.get('custom_id')

    # Если поле custom_id передано и это НЕ пустая строка
    if custom_id is not None and custom_id != '':

        # 1. Сначала проверяем, что это строка (защита от int, list, null)
        if not isinstance(custom_id, str):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )

        custom_id = custom_id.strip()

        # 2. Если после очистки от пробелов строка стала пустой — генерируем
        if not custom_id:
            custom_id = URLMap.get_unique_short_id()
        else:
            # 3. Проверяем длину и недопустимые символы
            if len(custom_id) > MAX_LENGTH_SHORT or not re.match(
                SHORT_ID_PATTERN, custom_id
            ):
                raise InvalidAPIUsage(
                    'Указано недопустимое имя для короткой ссылки'
                )

            # 4. Проверяем на занятость
            existing = URLMap.check_unique(custom_id)
            if custom_id == 'files' or existing:
                raise InvalidAPIUsage(
                    'Предложенный вариант короткой ссылки уже существует.'
                )
    else:
        # Если ключа нет или он равен "" — генерируем автоматически
        custom_id = URLMap.get_unique_short_id()

    urlmap = URLMap(
        original=original_url,
        short=custom_id
    )
    db.session.add(urlmap)
    db.session.commit()

    return jsonify(urlmap.to_dict()), HTTPStatus.CREATED
