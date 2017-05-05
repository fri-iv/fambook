from flask import Flask
from flask_socketio import SocketIO
import os
from flask import Flask

template_dir = os.path.abspath('templates')
static_dir = os.path.abspath('static')
app = Flask(__name__,
            template_folder=template_dir,
            static_folder=static_dir)
app.config.from_object(__name__)
app.secret_key = 'SdfhP(DS&yfpSIUdfgsidfhSFIUSgdfs'


socketio = SocketIO(app)

# from notes import views
# from users import views
from apps.facebook import views