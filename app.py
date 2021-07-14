from flask import Flask, render_template, request
import sqlite3
import textwrap
import pyodbc
import time
import os
import redis
import hashlib
import pickle

app = Flask(__name__)


driver = '{ODBC Driver 17 for SQL Server}'
server_name = 'assign1server'
database_name = 'assignment1'
server = 'tcp:database.windows.net,1433'
username = "saitheja"
password = "9705004946S@i"

r = redis.Redis(host='saitheja.redis.cache.windows.net',
                port=6380, db=0, password='UIO8izHCadRdL+fe6T5L04jCo+0JUMua4N0QIX2wbAw=',ssl=True)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/q5')
def q5():
   return render_template('q5.html')
@app.route('/q6')
def q6():
   return render_template('q6.html')


@app.route('/q8')
def q8():
   return render_template('q8.html')

@app.route('/q')
def q():
   return render_template('newrecord.html')








@app.route('/normalmag', methods=['POST','GET'])
def list1():
    
    e1=request.form['e1']
    e2=request.form['e2']
    
    
    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    querry1="Select  id,ptime,latitude,longitude,depth,mag,place,magType,etime  from q WHERE etime  between '"+e1+"' and '"+e2+"'"
    hash = hashlib.sha224(querry1.encode('utf-8')).hexdigest()
    key = "redis_cache:" + hash

    t1 = time.time()
    for i in range(1,500):
            crsr.execute(querry1)
            data = crsr.fetchall()
            r.set(key, pickle.dumps(data))
            r.expire(key,36)
    t2 = time.time()
    total=t2-t1
    cnxx.close()
    return render_template("opt.html",time = total)

@app.route('/mag', methods=['POST','GET'])
def list():
    
    e1=request.form['e1']
    e2=request.form['e2']
    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    querry1="Select  id,ptime,latitude,longitude,depth,mag,place,magType,etime  from q WHERE etime  between '"+e1+"' and '"+e2+"'"
    hash = hashlib.sha224(querry1.encode('utf-8')).hexdigest()
    key = "redis_cache:" + hash

    t1 = time.time()
    for i in range(1,500):
        if(r.get(key)):
            pass
        else:
            crsr.execute(querry1)
            data = crsr.fetchall()
            r.set(key, pickle.dumps(data))
            
            r.expire(key,36)
    t2 = time.time()
    total=t2-t1
    cnxx.close()
    return render_template("opt.html",time = total)


@app.route('/withoutredis', methods=['POST','GET'])
def withoutredis():
    
    m1=request.form['m1']
    m2=request.form['m2']
    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
   
    querry1="Select  id,ptime,latitude,longitude,depth,mag,place,magType,etime  from q WHERE mag  between '"+m1+"' and '"+m2+"' "
    hash = hashlib.sha224(querry1.encode('utf-8')).hexdigest()
    key = "redis_cache:" + hash

    t1 = time.time()
    for i in range(1,500):
            crsr.execute(querry1)
            data = crsr.fetchall()
            r.set(key, pickle.dumps(data))
            r.expire(key,36)
    t2 = time.time()
    total=t2-t1
    cnxx.close()
    return render_template("opt.html",time = total)

@app.route('/redis', methods=['POST','GET'])
def redismag():
    
    m1=request.form['m1']
    m2=request.form['m2']
    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    querry1="Select  id,ptime,latitude,longitude,depth,mag,place,magType,etime  from q WHERE mag  between '"+m1+"' and '"+m2+"'"
    hash = hashlib.sha224(querry1.encode('utf-8')).hexdigest()
    key = "redis_cache:" + hash

    t1 = time.time()
    for i in range(1,500):
        if(r.get(key)):
            pass
        else:
            crsr.execute(querry1)
            data = crsr.fetchall()
            r.set(key, pickle.dumps(data))
            
            r.expire(key,36)
    t2 = time.time()
    total=t2-t1
    cnxx.close()
    return render_template("opt.html",time = total)







if __name__ == '__main__':
    app.debug=True
    app.run()
    