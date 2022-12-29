from flask import render_template, request, redirect, url_for
from datetime import datetime
import os
from . import home_bp


@home_bp.route('/')
def index():
    return render_template("main.html",
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           time=datetime.now().strftime("%H:%M:%S"))


@home_bp.route("/about")
def about():
    return render_template("about.html",
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           time=datetime.now().strftime("%H:%M:%S"))


@home_bp.route("/info")
def info():
    return render_template("info.html",
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           time=datetime.now().strftime("%H:%M:%S"))

