from flask import g, request, render_template

from flask_backend import latest
from flask_backend.helper.decorator import limit


@latest.route('/', methods=['GET'])
@limit(requests=100, window=60, by="ip")
def index():
    return render_template('index.html')
