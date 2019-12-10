from flask import url_for


def send_reset_link(user):
    token = user.get_reset_token()
    link = url_for('reset_token', token=token, _external=True)
    print(link)
