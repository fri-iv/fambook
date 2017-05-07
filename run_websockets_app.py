from apps import app, socketio
from libs.router import load_routs
from db import Base, engine


@socketio.on('connect')
def connection():
    print 'connecting'


@socketio.on('message')
def message(data):
    print 'message:', data

def start():
    load_routs()
    Base.metadata.create_all(engine)
    # app.run(debug=True, host='0.0.0.0', port=5001)
    # print 'started HTTP'
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    print 'started websockets'


if __name__ == '__main__':
    start()
