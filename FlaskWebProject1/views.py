from datetime import datetime, timedelta
from flask import render_template, redirect, request
from FlaskWebProject1 import app
import mysql.connector as m


mc = m.connect(user='root', password='amaatra', database='smallproject', host='127.0.0.1')
cur = mc.cursor()
def updateandlog(trail, elem):
    if elem[0:2] == 'v1':
        abc = str(datetime.now().isoformat())[:10]
    elif elem[0:2] == 'v2':
        abc = str((datetime.now() + timedelta(days=1)).isoformat())[:10]
    cur.execute('update train set seat' + elem[2] + '= 1 where date = "' + abc + '"')     
    mc.commit()
    with open('log.txt', 'a+') as f:
        a = str((trail, elem, abc))
        a+= '\n'
        f.write(a)

def getseats(date):
    lst, c = [],0
    cur.execute('select * from train where date = "' + date + '"')
    for i in cur.fetchone():
        if c != 0:
            lst.append((not bool(int(i)), c))
        c+=1
    return lst

@app.route('/')
@app.route('/home')
def home():
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year
    )

@app.route('/contact')
def contact():
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year
    )

@app.route('/booking')
def booking():
    todayvis= getseats(str(datetime.now().isoformat())[:10])
    tomvis = getseats(str((datetime.now() + timedelta(days=1)).isoformat())[:10])
    return render_template(
        'booking.html',
        title='Booking',
        year=datetime.now().year,
        v1 = todayvis,
        v2 = tomvis
    )

@app.route('/tutorial')
def tutorial():
    return render_template(
        'tutorial.html',
        title='Tutorial',
        year=datetime.now().year
    )

@app.route('/submit', methods=["POST"])
def submit():
    if request.method == 'POST':
        information = request.form
        c = 0
        a = []
        a.append((information['BookerName'], information['ContactNo']))
        for i in information:
            if c > 1:
                updateandlog(a,i)
            c+=1


    return render_template(
        'submit.html',
        title='Result',
        year=datetime.now().year,
        data = information
    )
