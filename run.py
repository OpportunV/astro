from tasks.blueprint import tasks
from view import *

app.register_blueprint(tasks, url_prefix='/tasks')

if __name__ == '__main__':
    app.run()
