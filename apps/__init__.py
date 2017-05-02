from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'SdfhP(DS&yfpSIUdfgsidfhSFIUSgdfs'


socketio = SocketIO(app)

# from notes import views
# from users import views
from apps.facebook import views