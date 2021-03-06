import os

from flask import Flask
from flask_mail import Mail


mail = Mail()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'main.sqlite'),
        MAIL_SERVER='boss.staszic.waw.pl',
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import zapisy
    app.register_blueprint(zapisy.bp)
    app.add_url_rule('/', endpoint='index')

    from . import admin
    app.register_blueprint(admin.bp)
    admin.init_app(app)

    from . import obsluga_maili
    obsluga_maili.init_app(app)

    mail.init_app(app)

    @app.route('/henlo')
    def henlo():
        return 'Henlo , Warld!1'

    return app

app = create_app()
