#!/usr/bin/env python3
import cgi
import html

form = cgi.FieldStorage()
text1 = form.getfirst("TEXT_1", "не задано")
text2 = form.getfirst("TEXT_2", "не задано")
text1 = html.escape(text1)
text2 = html.escape(text2)


if form.getvalue("maths"):
    math_flag = "ON"
else:
    math_flag = "OFF"

if form.getvalue("physics"):
    physics_flag = "ON"
else:
    physics_flag = "OFF"

if form.getvalue('subject'):
    subject = form.getvalue('subject')
else:
    subject = "Not set"

print("Content-type: text/html\r\n\r\n")
print("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Обработка данных форм</title>
        </head>
        <body>""")

print("<p>TEXT_1: {}</p>".format(text1))
print("<p>TEXT_2: {}</p>".format(text2))
print("<h2> CheckBox Maths is : %s</h2>" % math_flag)
print("<h2> CheckBox Physics is : %s</h2>" % physics_flag)
print("<h2> Selected Subject is %s</h2>" % subject)
print("""</body>
        </html>""")
