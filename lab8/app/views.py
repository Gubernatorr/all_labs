from urllib.parse import urlparse, urljoin
from flask import Flask
from datetime import datetime
import os
from flask import render_template, request, session, redirect, url_for, flash
from flask_login import logout_user, login_required, current_user, login_user
from werkzeug.exceptions import abort
from app.forms import MyForm, RegistrationForm, LoginForm
from loguru import logger
from app import app, db
from app.models import Message, User

logger.add("logs.log")

menu = {
    "/": "Home",
    "/about": "About me",
    "/certifications": "My licenses & certifications",
    "/contact": "Contact"
}


@app.route('/')
def index():
    return render_template("main.html", menu=menu,
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           time=datetime.now().strftime("%H:%M:%S"))


@app.route('/main.html')
def main():
    return render_template("main.html", menu=menu,
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           time=datetime.now().strftime("%H:%M:%S"))


@app.route("/about")
def about():
    return render_template("about.html", menu=menu,
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           time=datetime.now().strftime("%H:%M:%S"))


@app.route("/info")
def info():
    return render_template("info.html", menu=menu,
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           time=datetime.now().strftime("%H:%M:%S"))


@app.route('/contact.html', methods=['GET', 'POST'])
def contact():
    form = MyForm()
    if form.validate_on_submit():
        logger.info(get_log_message(form))
        session['name'] = form.name.data
        session['email'] = form.email.data
        message = Message(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            subject=form.subject.data,
            message=form.message.data
        )
        try:
            db.session.add(message)
            db.session.commit()
        except:
            db.session.flush()
            db.session.rollback()
        flash(f"Your message has been sent: {form.name.data}, {form.email.data}", category='success')
        return redirect(url_for("contact"))
    elif request.method == 'POST':
        flash("Post method validation failed", category='warning')
        return render_template('contact.html', menu=menu, form=form, operating_system=os.name,
                               user_agent=request.user_agent,
                               time=datetime.now().strftime("%H:%M:%S"))

    form.name.data = session.get("name")
    form.email.data = session.get("email")
    return render_template('contact.html', menu=menu, form=form, operating_system=os.name,
                           user_agent=request.user_agent,
                           time=datetime.now().strftime("%H:%M:%S"))


def get_log_message(form):
    fields = (
        form.name.data,
        form.email.data,
        form.phone.data,
        form.subject.data,
        form.message.data
    )
    return " ".join(fields)


@app.route('/delete-message/<id>')
def delete_message(id):
    Message.query.filter_by(id=id).delete()
    try:
        db.session.commit()
    except:
        db.session.flush()
        db.session.rollback()
    return redirect(url_for("messages"))


@app.route('/messages.html')
def messages():
    messages = Message.query.all()
    return render_template('messages.html', messages=messages, menu=menu)


@app.route('/register.html', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        try:
            db.session.add(user)
            db.session.commit()
            flash(
                f"Account created for {form.username.data}!", category='success')
            return redirect(url_for("login"))
        except:
            db.session.flush()
            db.session.rollback()

    return render_template('register.html', menu=menu, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash("You have been logged in!", category="success")
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
            return redirect(url_for("index"))
        else:
            flash(f"Email or password is incorrect", category='danger')
    return render_template('login.html', menu=menu, form=form)


@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', menu=menu, users=users)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out!", category="warning")
    return redirect(url_for("login"))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', menu=menu)


@app.route('/delete-user/<id>')
def delete_user(id):
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
    except:
        db.session.flush()
        db.session.rollback()
    return redirect(url_for("users"))


if __name__ == '__main__':
    app.run(debug=True)
