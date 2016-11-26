from flask import session, render_template


def checklogin():
    if "username" in session:
        pass
    else:
        return render_template('login.html')
