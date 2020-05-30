from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from application import app, db, bcrypt
from application.auth.models import Account
from application.auth.forms import LoginForm, RegisterForm


@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm(), register_form = RegisterForm())

    form = LoginForm(request.form)
    if form.validate():
        user = db.session.query(Account).filter_by(name=form.name.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("campaigns_index"))

    return render_template("auth/loginform.html", form = form, register_form = RegisterForm(), error = "No such username or password")


@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("auth_login"))


@app.route("/auth/register", methods=["GET", "POST"])
def auth_register():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm(), register_form = RegisterForm())

    form = RegisterForm(request.form)
    if not form.validate():
        return render_template("auth/loginform.html", form = LoginForm(), register_form = form)

    user = db.session.query(Account).filter_by(name=form.register_name.data).first()
    if user:
        return render_template("auth/loginform.html", form = LoginForm(), register_form = form,
                               register_error = "Account name is already taken")

    account_to_add = Account(form.register_name.data, form.register_password.data)
    db.session().add(account_to_add)
    db.session().commit()

    return redirect(url_for("auth_login"))

