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

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register/',methods=['GET','POST'])
def register_page():
    if request.method=='POST':
        cur,conn=connection()
        cur.execute('CREATE TABLE IF NOT EXISTS users (user_id NUMBER, user_name TEXT, name TEXT, email TEXT, password TEXT, settings TEXT)')
        conn.commit()
        user_name=request.form['user_name']
        cur.execute('SELECT COUNT (*) FROM users WHERE user_name=?',(user_name,))
        count=cur.fetchone()[0]
        if count==0:
            cur.execute('SELECT COUNT (*) FROM users')
            next_user_id=cur.fetchone()[0]+1
            name=request.form['name']
            email=request.form['email']
            password=request.form['password']
            cur.execute('INSERT INTO users VALUES (?,?,?,?,?,?)',(next_user_id,user_name,name,email,password,'NULL'))
            conn.commit()
            session['logged_in']=True
            session['user_id']=next_user_id
            session['user_name']=user_name
            session['name']=name
            session['settings']='NULL'
            return redirect(url_for('board',num=1))
        else:
            error="This user name has already been taken. Please choose another."
            return render_template('register.html',error=error)
    else:
        return render_template('register.html')

@app.route('/login/',methods=['GET','POST'])
def login_page():
    if request.method=='POST':
        cur,conn=connection()
        cur.execute('CREATE TABLE IF NOT EXISTS users (user_id NUMBER, user_name TEXT, name TEXT, email TEXT, password TEXT, settings TEXT)')
        conn.commit()
        user_name=request.form['user_name']
        cur.execute('SELECT COUNT (*) FROM users WHERE user_name=?',(user_name,))
        count=cur.fetchone()[0]
        if count==0:
            error="Invalid credentials. Please try again."
            return render_template('login.html',error=error)
        else:
            password=request.form['password']
            cur.execute('SELECT * FROM users WHERE user_name=?',(user_name,))
            data=cur.fetchall()[0]
            if password==data[4]:
                session['logged_in']=True
                session['user_name']=user_name
                session['user_id']=data[0]
                session['name']=data[2]
                session['settings']=data[5]
                return redirect(url_for('board',num=1))
            else:
                error="Invalid credentials. Please try again."
                return render_template('login.html',error=error)
    else:
        return render_template('login.html')


@app.route('/board/<int:num>/')
@login_required
def board(num):
    try:
        cur,conn=connection()
        cur.execute('SELECT COUNT (*) FROM posts')
        count=cur.fetchone()[0]
        no_of_pages=(count/10)+1
        current=num
        if count>10:
            if num==1:
                start=count-10
            else:
                start=count-(int(num))*10
            end=start+10
        else:
            start=0
            end=10
        cur.execute('SELECT * FROM posts WHERE s_no>? AND s_no<=? ORDER BY s_no DESC',(start,end))
        data=cur.fetchall()
        return render_template('board.html',data=data,no_of_pages=no_of_pages, current=current, posts_on_page=len(data))
    except Exception as e:
        return str(e)

@app.route('/sell/',methods=['GET','POST'])
@login_required
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
        cur.execute('INSERT INTO posts VALUES (?,?,?,?,?,?,?,?)',(count+1,'S',next_tr_id,session['user_id'],content,selling_p,used_for,add_info))
        conn.commit()
        return redirect(url_for('board',num=1))
        #return redirect (url_for('board',num=1))
    else:
        return render_template('sell.html')

@app.route('/seek/',methods=['GET','POST'])
@login_required
def seek():
    if request.method=='POST':
        cur,conn=connection()
        content=request.form['content']
        add_info=request.form['add_info']
        cur.execute('SELECT COUNT (*) FROM posts')
        count=cur.fetchone()[0]
        cur.execute('SELECT tr_id FROM posts WHERE s_no=?',(count,))
        next_tr_id=cur.fetchone()[0]+1
        cur.execute('INSERT INTO posts VALUES (?,?,?,?,?,?,?,?)',(count+1,'R',next_tr_id,session['user_id'],content,'NULL','NULL',add_info))
        conn.commit()
        return redirect(url_for('board',num=1))
    else:
        return render_template('seek.html')



@app.route('/post/<int:tr_id>/')
def post(tr_id):
    return str(tr_id)

@app.route('/logout/')
@login_required
def logout():
    session.clear()
    #flash('You are now logged out')
    return redirect(url_for('index'))

if __name__=="__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
