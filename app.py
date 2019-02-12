import numpy as np
from pathlib import Path
#Flask liblaries
from flask import Flask, flash, redirect, render_template, request, session, abort
#Sql liblaries
from sqlalchemy.orm import sessionmaker
import sqlite3 as sql
#My own helper liblaries
import sketcher as skt
import mach as mch

import os
from tabledef import *
engine = create_engine('sqlite:///tutorial.db', echo=True)

app = Flask(__name__)

@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        POST_USERNAME = str(request.form['username'])
        POST_PASSWORD = str(request.form['password'])
 
        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
        result = query.first()
        if result:
            session['logged_in'] = True
        else:
            flash('wrong password!')
        return index()
    else:
        return render_template("login.html")

@app.route("/logout",methods = ['POST', 'GET'])
def logout():
    if request.method == "POST":
        session['logged_in'] = False
        return index()
    else:
        return render_template("index.html")

@app.route("/")
@app.route("/index")
def index():
    dane = {"tytul":"Strona główna","tresc":"brak tresci"}
    return render_template("index.html",tytul=dane['tytul'],tresc=dane['tresc'])

@app.route('/dodaj',methods = ['POST', 'GET'])
def dodaj():
	try:
		if request.method == 'POST':
			if request.form['submit'] == 'dodaj':
				new1 = skt.draw()
				new2 = mch.Machine_learning()
				path,img = new1.main()
				print('fdd')				
				tytul = request.form['tytul']
				autor = request.form['autor']
				label1 = request.form['label1']
				label2 = request.form['label2']
				
				print(new2.main())
				conn = sql.connect('./database.db')
				cur = conn.cursor()
				cur.execute('INSERT INTO images(tytul,autor,label1,label2,path,data) VALUES (?,?,?,?,?,current_timestamp)',(tytul,autor,label1,label2,path))
				conn.commit()
		elif request.method == 'GET':
			pass
	except:
		conn.rollback()
	finally:
		return render_template("dodaj.html")
		conn.close()

@app.route('/register',methods = ['POST', 'GET'])
def register():
    if request.method == "POST":
        POST_USERNAME = str(request.form['username'])
        POST_PASSWORD = str(request.form['password'])
        Session = sessionmaker(bind=engine)
        session = Session()
        user = User(POST_USERNAME,POST_PASSWORD)
        session.add(user)
        session.commit()
        return render_template("index.html")
    else:
        return render_template("register.html")

@app.route("/usun",methods = ['POST', 'GET'])
def usun():
    if request.method == 'POST':
        id = request.form['usun']
        conn = sql.connect('./database.db')
        cur = conn.cursor()
        cur.execute('DELETE FROM images where rowid=?',id)
        conn.commit()
    con = sql.connect("./database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('SELECT rowid,tytul,autor,label1,label2,path,data FROM images')
    rekordy = cur.fetchall();
    return render_template("usun.html",rekordy = rekordy)

@app.route('/lista')
def list():
    con = sql.connect("./database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('SELECT * FROM images')
    rekordy = cur.fetchall();
    return render_template("lista.html",rekordy = rekordy)

if __name__ == '__main__':
	app.secret_key = os.urandom(12)
	app.run(debug = True)