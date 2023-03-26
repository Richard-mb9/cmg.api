import flask
from flask_cors import CORS
from flask import Flask
from sqlalchemy.orm import Session, sessionmaker

from src.infra.http.routes import create_routes


def create_app():
    app = Flask(__name__)
    CORS(app)

    create_routes(app)

    return app


app = create_app()


@app.teardown_appcontext
def teardown(e):
    g = flask.g
    if 'session' in g:
        session: Session = g.get('session')
        session.close()
        session.remove()


@app.before_request
def load_session():
    from src.config import get_engine
    from sqlalchemy.orm import scoped_session
    engine = get_engine()
    Session = scoped_session(sessionmaker(
        autocommit=False, autoflush=False, bind=engine))
    flask.g.session = Session


@app.route('/docs')
def docs():  # pragma: no cover
    import os
    from flask import Response
    path = os.path.abspath('redoc-static.html')
    arq = open(path, 'r')
    return Response(response=arq)


@app.route('/image/<bucket_name>/<filename>')
def image(bucket_name, filename):  # pragma: no cover
    import os
    from flask import send_file
    path = os.path.abspath(f'upload/{bucket_name}/{filename}')
    return send_file(path)
