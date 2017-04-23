from apps import app
from libs.router import load_routs

load_routs()
app.run(debug=True, host='0.0.0.0', port=5000)
