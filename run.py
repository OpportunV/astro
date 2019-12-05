from tasks.blueprint import tasks
from view import *

app.register_blueprint(tasks, url_prefix='/tasks')

if __name__ == '__main__':
    app.run(debug=True)
    # from waitress import serve
    # serve(app, host='127.0.0.1', port=5000)
