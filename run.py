from unix.blueprint import tasks
from view import *

app.register_blueprint(tasks, url_prefix='/unix')

if __name__ == '__main__':
    app.run()
