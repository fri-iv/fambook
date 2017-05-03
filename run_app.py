from apps import app, socketio
from libs.router import load_routs
from db import Base, engine


def start():
    load_routs()
    Base.metadata.create_all(engine)
    # app.run(debug=True, host='0.0.0.0', port=5000)
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    start()
