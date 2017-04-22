from apps import app
from libs.router import create_routs

create_routs()
app.run(debug=True)
