from flask import Flask

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'SdfhP(DS&yfpSIUdfgsidfhSFIUSgdfs'

from notes import views
from users import views