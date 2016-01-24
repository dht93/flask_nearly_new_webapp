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
        cur.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, user_name TEXT, name TEXT, contact TEXT, email TEXT, password TEXT, settings TEXT)')
        conn.commit()
        user_name=request.form['user_name']
        cur.execute('SELECT COUNT (*) FROM users WHERE user_name=?',(user_name,))
        count=cur.fetchone()[0]
        if count==0:
            name=request.form['name']
            email=request.form['email']
            password=request.form['password']
            settings='00'
            cur.execute('INSERT INTO users (user_name, name, contact, email, password, settings) VALUES (?,?,?,?,?,?)',(user_name,name,'NULL',email,password,settings))
            conn.commit()
            cur.execute('SELECT user_id FROM users WHERE user_name=?',(user_name,))
            user_id=cur.fetchone()[0]
            session['logged_in']=True
            session['user_id']=user_id
            session['user_name']=user_name
            session['name']=name
            session['settings']=settings
            session['email']=email
            session['contact']='NULL'
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
        cur.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, user_name TEXT, name TEXT, contact TEXT, email TEXT, password TEXT, settings TEXT)')
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
            if password==data[5]:
                session['logged_in']=True
                session['user_name']=user_name
                session['user_id']=data[0]
                session['name']=data[2]
                session['settings']=data[6]
                session['email']=data[4]
                session['contact']=data[3]
                return redirect(url_for('board',num=1))
            else:
                error="Invalid credentials. Please try again."
                return render_template('login.html',error=error)
    else:
        return render_template('login.html')


@app.route('/board/<int:num>/')
@login_required
def board(num):
    cur,conn=connection()
    cur.execute('CREATE TABLE IF NOT EXISTS posts (tr_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, type TEXT,user_id TEXT,content TEXT,selling_p TEXT,used_for TEXT, add_info TEXT)')
    conn.commit()
    cur.execute('SELECT COUNT (*) FROM posts')
    count=cur.fetchone()[0]
    if count<=10:
        no_of_pages=1
    else:
        no_of_pages=(count/10)+1
    current=num
    if count>10:
        if num==1:
            start=count-10
        else:
            start=count-num*10
        end=start+10
    else:
        start=0
        end=10
    cur.execute('SELECT tr_id, type, users.name, content, selling_p, used_for, add_info, users.user_id FROM posts,users WHERE posts.user_id=users.user_id AND tr_id>? AND tr_id<=? ORDER BY tr_id DESC',(start,end))
    data=cur.fetchall()
    return render_template('board.html',data=data,no_of_pages=no_of_pages, current=current, posts_on_page=len(data))

@app.route('/sell/',methods=['GET','POST'])
@login_required
def sell():
    if request.method =='POST':

        cur,conn=connection()
        content=request.form['content']
        selling_p=request.form['selling_p']
        used_for=request.form['used_for']
        add_info=request.form['add_info']
        if len(add_info)==0:
            add_info='NULL'
        cur.execute('INSERT INTO posts (type, user_id, content, selling_p, used_for, add_info) VALUES (?,?,?,?,?,?)',('S',session['user_id'],content,selling_p,used_for,add_info))
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
        if len(add_info)==0:
            add_info='NULL'
        cur.execute('INSERT INTO posts (type, user_id, content, selling_p, used_for, add_info) VALUES (?,?,?,?,?,?)',('R',session['user_id'],content,'NULL','NULL',add_info))
        conn.commit()
        return redirect(url_for('board',num=1))
    else:
        return render_template('seek.html')


@app.route('/settings/',methods=['GET','POST'])
@login_required
def settings():
    if request.method=='POST':
        cur,conn=connection()
        email=request.form['email']
        contact=request.form['contact']
        num_s=request.form['num_s']
        email_s=request.form['email_s']
        settings=''
        if num_s=='y':
            if session['contact']=='NULL':
                if len(contact)==0:
                    error='You want your contact number to be displayed on your posts by default. You need to provide a contact number for that.'
                    cur.execute('SELECT settings FROM users WHERE user_id=?',(session['user_id'],))
                    settings=cur.fetchone()[0]
                    return render_template('settings.html',error=error,settings=settings, message=None)
                else:
                    update=1
                    to_save=contact
                    settings+='1'
            else:
                if len(contact)==0:
                    update=0
                    settings+='1'
                else:
                    update=1
                    to_save=contact
                    settings+='1'
        else:
            if session['contact']=='NULL':
                if len(contact)==0:
                    update=0
                    settings+='0'
                else:
                    update=1
                    settings+='0'
            else:
                if len(contact)==0:
                    update=0
                    settings+='0'
                else:
                    update=1
                    settings+='0'
        if email_s=='y':
            if len(email)==0:
                update1=0
                settings+='1'
            else:
                update1=1
                settings+='1'
        else:
            if len(email)==0:
                update1=0
                settings+='0'
            else:
                update1=1
                settings+='0'
        cur,conn=connection()
        if update==0 and update1==0:
            cur.execute('UPDATE users SET settings=? WHERE user_id=?',(settings,session['user_id']))
        elif update==0 and update1==1:
            cur.execute('UPDATE users SET email=?, settings=? WHERE user_id=?',(email,settings,session['user_id']))
            session['email']=email
        elif update==1 and update1==0:
            cur.execute('UPDATE users SET contact=?, settings=? WHERE user_id=?',(contact,settings,session['user_id']))
            session['contact']=contact
        else:
            cur.execute('UPDATE users SET contact=?,email=?,settings=? WHERE user_id=?',(contact,email,settings,session['user_id']))
            session['contact']=contact
            session['email']=email
        conn.commit()
        message="Settings saved."
        return render_template('settings.html',settings=settings,message=message)
    else:
        cur,conn=connection()
        cur.execute('SELECT settings FROM users WHERE user_id=?',(session['user_id'],))
        settings=cur.fetchone()[0]
        message=None
        return render_template('settings.html',settings=settings,message=None)


@app.route('/your_posts/')
@login_required
def your_posts():
    try:
        cur,conn=connection()
        cur.execute('SELECT * FROM posts WHERE user_id=? ORDER BY tr_id DESC',(session['user_id'],))
        data=cur.fetchall()
        return render_template('your_posts.html',data=data)
    except Exception as e:
        return str(e)

@app.route('/post/<int:tr_id>/')
def post(tr_id):
    cur,conn=connection()
    cur.execute('SELECT tr_id, type, posts.user_id, users.name, users.contact, users.email, users.settings, content, selling_p, used_for, add_info FROM posts,users WHERE users.user_id=posts.user_id AND tr_id=?',(tr_id,))
    data=cur.fetchall()[0]
    cur.execute('CREATE TABLE IF NOT EXISTS requests_c (tr_id NUMBER, requestor NUMBER)')
    conn.commit()
    cur.execute('CREATE TABLE IF NOT EXISTS requests_e (tr_id NUMBER, requestor NUMBER)')
    conn.commit()
    cur.execute('SELECT COUNT (*) FROM requests_c WHERE tr_id=? AND requestor=?',(tr_id,session['user_id']))
    r_c=cur.fetchone()[0]
    cur.execute('SELECT COUNT (*) FROM requests_e WHERE tr_id=? AND requestor=?',(tr_id,session['user_id']))
    r_e=cur.fetchone()[0]
    request_data=[r_c,r_e]
    return render_template('post.html',data=data,request_data=request_data)


@app.route('/remove_post/<int:tr_id>/')
@login_required
def remove_post(tr_id):
    cur,conn=connection()
    cur.execute('DELETE FROM posts WHERE tr_id=?',(tr_id,))
    conn.commit()
    return redirect(url_for('your_posts'))

@app.route('/request/num/<int:tr_id>/')
@login_required
def request_num(tr_id):
    cur,conn=connection()
    cur.execute('CREATE TABLE IF NOT EXISTS requests_c (tr_id NUMBER, requestor NUMBER)')
    conn.commit()
    cur.execute('INSERT INTO requests_c VALUES (?,?)',(tr_id,session['user_id']))
    conn.commit()
    message="Request sent"
    cur.execute('SELECT tr_id, type, posts.user_id, users.name, users.contact, users.email, users.settings, content, selling_p, used_for, add_info FROM posts,users WHERE users.user_id=posts.user_id AND tr_id=?',(tr_id,))
    data=cur.fetchall()[0]
    cur.execute('SELECT COUNT (*) FROM requests_c WHERE tr_id=? AND requestor=?',(tr_id,session['user_id']))
    r_c=cur.fetchone()[0]
    cur.execute('SELECT COUNT (*) FROM requests_e WHERE tr_id=? AND requestor=?',(tr_id,session['user_id']))
    r_e=cur.fetchone()[0]
    request_data=[r_c,r_e]
    return render_template('post.html',message=message, data=data, request_data=request_data)

@app.route('/request/email/<int:tr_id>/')
@login_required
def request_email(tr_id):
    cur,conn=connection()
    cur.execute('CREATE TABLE IF NOT EXISTS requests_e (tr_id NUMBER, requestor NUMBER)')
    conn.commit()
    cur.execute('INSERT INTO requests_e VALUES (?,?)',(tr_id,session['user_id']))
    conn.commit()
    message="Request sent"
    cur.execute('SELECT tr_id, type, posts.user_id, users.name, users.contact, users.email, users.settings, content, selling_p, used_for, add_info FROM posts,users WHERE users.user_id=posts.user_id AND tr_id=?',(tr_id,))
    data=cur.fetchall()[0]
    cur.execute('SELECT COUNT (*) FROM requests_c WHERE tr_id=? AND requestor=?',(tr_id,session['user_id']))
    r_c=cur.fetchone()[0]
    cur.execute('SELECT COUNT (*) FROM requests_e WHERE tr_id=? AND requestor=?',(tr_id,session['user_id']))
    r_e=cur.fetchone()[0]
    request_data=[r_c,r_e]
    return render_template('post.html',message=message, data=data, request_data=request_data)

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
