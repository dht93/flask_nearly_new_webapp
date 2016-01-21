from flask import Flask, render_template,request, url_for, redirect, session
import sqlite3
from functools import wraps

app=Flask(__name__)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            return redirect (url_for('login_page'))
    return wrap

def connection():
    conn=sqlite3.connect('users.sqlite')
    cur=conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS posts (s_no NUMBER, type TEXT, tr_id NUMBER, user_id NUMBER, content TEXT, selling_p NUMBER, used_for TEXT, add_info TEXT)')
    conn.commit()
    return (cur,conn)

@app.route('/board/<num>/')
#@login_required
def board(num):
    try:
        cur,conn=connection()
        start=(int(num)-1)*10
        end=start+10
        cur.execute('SELECT * FROM posts WHERE s_no>? AND s_no<=?',(start,end))
        data=cur.fetchall()
        return render_template('board.html',data=data)
    except Exception as e:
        return str(e)

@app.route('/sell/')
@login_required
def sell():
    try:
        cur,conn=connection()

        content=request.form['content']
        selling_p=request.form['selling_p']
        used_for=request.form['used_for']
        add_info=request.form['add_info']

        cur.execute('SELECT COUNT (*) FROM posts')

        count=cur.fetchone()[0]
        if not count==0:
            cur.execute('SELECT tr_id FROM posts WHERE s_no=?',(count,))
            next_tr_id=cur.fetchone()[0]+1
        else:
            count=1
            next_tr_id=5555
        cur.execute('INSERT INTO posts VALUES (?,?,?,?,?,?,?,?)',(count+1,'S',next_tr_id,session['user_id'],content,selling_p,used_for,add_info))
        conn.commit()
        return redirect (url_for('board'))
    except Exceptipn as e:
        return str(e)

@app.route('/request/')
@login_required
def request():
    try:
        cur,conn=connection()
        content=request.form['content']
        exp_price=request.form['exp_price']
        add_info=request.form['add_info']
        cur.execute('SELECT COUNT (*) FROM posts')
        count=cur.fetchone()[0]
        if not count==0:
            cur.execute('SELECT tr_id FROM posts WHERE s_no=?',(count,))
            next_tr_id=cur.fetchone()[0]+1
        else:
            count=1
            next_tr_id=5555
        cur.execute('INSERT INTO posts VALUES (?,?,?,?,?,?,?,?)',(count+1,'R',next_tr_id,session['user_id'],content, exp_price,'NULL',add_info))
        conn.commit()
        return redirect(url_for('board'))
    except Exception as e:
        return str(e)

if __name__=="__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
