from flask import Flask, Blueprint

latest = Blueprint('latest', __name__)


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config_name)

    # treat /some/url/ and /some/url the same
    app.url_map.strict_slashes = False

    # server-level interface
    from flask_backend.interface import request_life_cycle

    # app lever interface
    from flask_backend.interface import route

    app.register_blueprint(latest)

    return app
