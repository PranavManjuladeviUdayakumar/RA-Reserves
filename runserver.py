"""
This script runs the FlaskWebProject1 application using a development server.
"""

from os import environ
from FlaskWebProject1 import app
import mysql.connector as m
from datetime import datetime, timedelta


if __name__ == '__main__':
    mc = m.connect(user='root', password='amaatra', database='smallproject', host='127.0.0.1')
    cur = mc.cursor()
    cur.execute("create table if not exists train(date date not null, seat1 bool default 0 not null, seat2 bool default 0 not null, seat3 bool default 0 not null, seat4 bool default 0 not null, seat5 bool default 0 not null, seat6 bool default 0 not null, seat7 bool default 0 not null, seat8 bool default 0 not null, seat9 bool default 0 not null, seat10 bool default 0 not null)")
    today, tomorrow=str(datetime.now().isoformat()), str((datetime.now() + timedelta(days=1)).isoformat())
    s1, s2 = 'select * from train where date = "' + today[:10] + '"', 'select * from train where date = "' +tomorrow[:10] + '"'
    s3, s4 = 'insert into train values("' + today[:10] + '",0,0,0,0,0,0,0,0,0,0)', 'insert into train values("' + tomorrow[:10] + '",0,0,0,0,0,0,0,0,0,0)'
    cur.execute(s1)
    if cur.fetchone() == None:
        cur.execute(s3)
    cur.execute(s2)
    if cur.fetchone() == None:
        cur.execute(s4)
    mc.commit()
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)

