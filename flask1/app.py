import os
from datetime import datetime

from flask import Flask, render_template, request

# create the object of Flask
app = Flask(__name__)
menu = {
    "/": "Home",
    "/index": "Home",
    "/contact": "Contact"
}


# creating our routes
@app.route('/')
def index():
    data = "Codeloop"
    return render_template('index.html', data=data, menu=menu,
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           time=datetime.now().strftime("%H:%M:%S"))


# creating our routes
@app.route('/index.html')
def Code():
    data = "Codeloop"
    return render_template('index.html', data=data,  menu=menu,
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           time=datetime.now().strftime("%H:%M:%S"))


# contact routes
@app.route('/contact.html')
def Contact():
    return render_template('contact.html',  menu=menu,
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           time=datetime.now().strftime("%H:%M:%S"))


@app.route('/base.html')
def Home():
    return render_template('base.html',  menu=menu,
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           time=datetime.now().strftime("%H:%M:%S"))


# run flask app
if __name__ == "__main__":
    app.run(debug=True)
