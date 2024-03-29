from tasks.blueprint import tasks
from users.view import users
from errors.view import errors
from view import *

app.register_blueprint(tasks, url_prefix='/tasks')
app.register_blueprint(users)
app.register_blueprint(errors)

if __name__ == '__main__':
    app.run(debug=True)
    # from waitress import serve
    # serve(app, host='127.0.0.1', port=5000)
