import re
from flask import jsonify, request, url_for
from .error_handlers import InvalidAPIUsage
from . import app, db
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    urlmap = URLMap.query.filter_by(short=short_id.strip()).first()
    if not urlmap:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': urlmap.original}), 200


@app.route('/api/id/', methods=['POST'])
def create_url():
    data = request.get_json(force=True, silent=True)
    if not data or not isinstance(data, dict):
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    original_url = data['url'].strip()

    custom_id = data.get('custom_id')

    if custom_id:
        custom_id = custom_id.strip()

        if len(custom_id) > 16 or not re.match(r'^[a-zA-Z0-9_-]+$', custom_id):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )

        if (
            custom_id == 'files'
            or URLMap.query.filter_by(short=custom_id).first()
        ):
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )
    else:
        custom_id = get_unique_short_id()

    urlmap = URLMap(
        original=original_url,
        short=custom_id
    )
    db.session.add(urlmap)
    db.session.commit()

    short_link = url_for(
        'redirect_view', short_id=urlmap.short, _external=True
    )

    return jsonify({
        'url': urlmap.original,
        'short_link': short_link
    }), 201
