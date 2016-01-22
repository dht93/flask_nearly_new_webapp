from flask import Flask, render_template,request, url_for, redirect, session, flash
import sqlite3
from functools import wraps
import gc

app=Flask(__name__)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            #flash("You need to login first")
            return redirect (url_for('login_page'))
    return wrap

def connection():
    conn=sqlite3.connect('users.sqlite')
    cur=conn.cursor()
    return (cur,conn)

@app.route('/board/<int:num>/')
#@login_required
def board(num):
    try:
        cur,conn=connection()
        cur.execute('SELECT COUNT (*) FROM posts')
        count=cur.fetchone()[0]
        if count>10:
            if num==1:
                start=count-10
            else:
                start=count-(int(num)-1)*10
            end=start+10
        else:
            start=0
            end=10
        cur.execute('SELECT * FROM posts WHERE s_no>? AND s_no<=? ORDER BY s_no DESC',(start,end))
        data=cur.fetchall()
        return render_template('board.html',data=data)
    except Exception as e:
        return str(e)

@app.route('/sell/',methods=['GET','POST'])
#@login_required
def sell():
    if request.method =='POST':

        cur,conn=connection()
        content=request.form['content']
        selling_p=request.form['selling_p']
        used_for=request.form['used_for']
        add_info=request.form['add_info']

        cur.execute('SELECT COUNT (*) FROM posts')

        count=cur.fetchone()[0]
        if not count==0:        #stuff present in posts
            cur.execute('SELECT tr_id FROM posts WHERE s_no=?',(count,))
            next_tr_id=cur.fetchone()[0]+1
        else:
            count=1
            next_tr_id=5555
        cur.execute('INSERT INTO posts VALUES (?,?,?,?,?,?,?,?)',(count+1,'S',next_tr_id,5,content,selling_p,used_for,add_info))
        conn.commit()
        return "Yo"
        #return redirect (url_for('board',num=1))
    else:
        return render_template('sell.html')

@app.route('/post/<int:tr_id>/')
def post(tr_id):
    return str(tr_id)

if __name__=="__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
