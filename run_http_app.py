from apps import app, socketio
from libs.router import load_routs
from db import Base, engine
from flask.templating import render_template


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/home')
def home():
    return render_template('home.html')


def start():
    # load_routs()
    Base.metadata.create_all(engine)
    app.run(debug=True, host='0.0.0.0', port=5001)
    print 'started HTTP'
    # socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    # print 'started websockets'

if __name__ == '__main__':
    start()
