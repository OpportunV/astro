from flask import Flask

from tasks.blueprint import tasks


app = Flask(__name__)
app.config['SECRET_KEY'] = '94427404642d31c91f64a75b977303a9'

app.register_blueprint(tasks, url_prefix='/tasks')
