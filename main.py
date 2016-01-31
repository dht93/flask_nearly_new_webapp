from flask import Flask, render_template,request, url_for, redirect, session, flash
import sqlite3
from functools import wraps
from passlib.hash import sha256_crypt


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

def get_notifs():
    cur,conn=connection()
    cur.execute('CREATE TABLE IF NOT EXISTS requests (request_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, tr_id NUMBER, type TEXT, requestor NUMBER, requestor_name TEXT, recipient NUMBER, recipient_name TEXT, response TEXT, ack TEXT, content TEXT)')
    conn.commit()
    cur.execute('CREATE TABLE IF NOT EXISTS help_out (help_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,tr_id NUMBER, helper_id NUMBER, helper_name TEXT, helped_id NUMBER, content TEXT, data_sent TEXT, ack TEXT)')
    conn.commit()
    #recipient_new_notifs
    cur.execute('SELECT COUNT (*) FROM requests WHERE recipient=? AND response=? ORDER BY request_id DESC',(session['user_id'],'NY'))
    rec=cur.fetchone()[0]
    #requestor_new_notifs
    cur.execute('SELECT COUNT (*) FROM requests WHERE requestor=? AND ack=? ORDER BY request_id DESC',(session['user_id'],'NS'))
    req=cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM help_out where helped_id=? AND ack=?',(session['user_id'],'NY'))
    helped_new=cur.fetchone()[0]
    cur.close()
    conn.close()
    notif_count=rec+req+helped_new
    return notif_count

@app.route('/')
def index():
    notif_count=0
    if session.get('logged_in',-1)==True:
        notif_count=get_notifs()
    return render_template('home.html',notif_count=notif_count)

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
            password=sha256_crypt.encrypt(str(request.form['password']))
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
            cur.close()
            conn.close()
            return redirect(url_for('index'))
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
            cur.close()
            conn.close()
            return render_template('login.html',error=error)
        else:
            password=request.form['password']
            cur.execute('SELECT * FROM users WHERE user_name=?',(user_name,))
            data=cur.fetchall()[0]
            if sha256_crypt.verify(password,data[5]):
                session['logged_in']=True
                session['user_name']=user_name
                session['user_id']=data[0]
                session['name']=data[2]
                session['settings']=data[6]
                session['email']=data[4]
                session['contact']=data[3]
                cur.close()
                conn.close()
                return redirect(url_for('board',num=1))
            else:
                cur.close()
                conn.close()
                error="Invalid credentials. Please try again."
                return render_template('login.html',error=error)
    else:
        return render_template('login.html')


@app.route('/board/<int:num>/',methods=['GET','POST'])
@login_required
def board(num):
    if request.method=='POST':
        cur,conn=connection()
        cur.execute('CREATE TABLE IF NOT EXISTS help_out (help_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,tr_id NUMBER, helper_id NUMBER, helper_name TEXT, helped_id NUMBER, content TEXT, data_sent TEXT, ack TEXT)')
        conn.commit()
        resp=request.form['num_s']
        number=request.form.get('number',-1)
        if not number==-1:
            cur.execute('UPDATE USERS SET contact=? WHERE user_id=?',('number',session['user_id']))
            conn.commit()
            session['contact']=number
        els=resp.split(',')
        if els[0]=='n':
            data_sent=session['email']
        else:
            data_sent=session['contact']+','+session['email']

        tr_id=els[1]
        helped_id=els[2]
        content=els[4]
        ack='NY'
        cur.execute('INSERT INTO help_out (tr_id, helper_id, helper_name,helped_id, content, data_sent, ack) VALUES(?,?,?,?,?,?,?)',(tr_id, session['user_id'], session['user_name'],helped_id, content, data_sent, ack))
        conn.commit()
        notif_count=get_notifs()
        return redirect(url_for('board',num=num))
    else:
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
        start=(num-1)*10
        end=start+10
        cur.execute('SELECT tr_id, type, users.name, content, selling_p, used_for, add_info, users.user_id FROM posts,users WHERE posts.user_id=users.user_id ORDER BY tr_id DESC LIMIT ?,?',(start,end))
        data=cur.fetchall()
        cur.close()
        conn.close()
        notif_count=get_notifs()
        print data[1][2],session['user_name']
        return render_template('board.html',data=data,no_of_pages=no_of_pages, current=current, posts_on_page=len(data),notif_count=notif_count)

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
        cur.close()
        conn.close()
        return redirect(url_for('board',num=1))
        #return redirect (url_for('board',num=1))
    else:
        cur,conn=connection()
        cur.execute('SELECT contact FROM users WHERE user_id=?',(session['user_id'],))
        contact=cur.fetchone()[0]
        cur.close()
        conn.close()
        notif_count=get_notifs()
        return render_template('sell.html',contact=contact,notif_count=notif_count)

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
        cur.close()
        conn.close()
        return redirect(url_for('board',num=1))
    else:
        cur,conn=connection()
        cur.execute('SELECT contact FROM users WHERE user_id=?',(session['user_id'],))
        contact=cur.fetchone()[0]
        cur.close()
        conn.close()
        notif_count=get_notifs()
        return render_template('seek.html',contact=contact,notif_count=notif_count)


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
                    notif_count=get_notifs()
                    return render_template('settings.html',error=error,settings=settings, message=None,notif_count=notif_count)
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
        message="Settings saved"
        cur.close()
        conn.close()
        notif_count=get_notifs()
        return render_template('settings.html',settings=settings,message=message,notif_count=notif_count)
    else:
        cur,conn=connection()
        cur.execute('SELECT settings FROM users WHERE user_id=?',(session['user_id'],))
        settings=cur.fetchone()[0]
        message=None
        cur.close()
        conn.close()
        notif_count=get_notifs()
        return render_template('settings.html',settings=settings,message=None,notif_count=notif_count)


@app.route('/your_posts/')
@login_required
def your_posts():
    cur,conn=connection()
    cur.execute('SELECT * FROM posts WHERE user_id=? ORDER BY tr_id DESC',(session['user_id'],))
    data=cur.fetchall()
    cur.close()
    conn.close()
    notif_count=get_notifs()
    return render_template('your_posts.html',data=data,notif_count=notif_count)


@app.route('/post/<int:tr_id>/')
def post(tr_id):
    cur,conn=connection()
    cur.execute('SELECT tr_id, type, posts.user_id, users.name, users.contact, users.email, users.settings, content, selling_p, used_for, add_info FROM posts,users WHERE users.user_id=posts.user_id AND tr_id=?',(tr_id,))
    data=cur.fetchall()[0]
    cur.execute('CREATE TABLE IF NOT EXISTS requests (request_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, tr_id NUMBER, type_r TEXT, requestor NUMBER, requestor_name TEXT, recipient NUMBER, recipient_name TEXT, response TEXT, ack TEXT, content TEXT)')
    conn.commit()
    cur.execute('SELECT COUNT(*), response FROM requests WHERE tr_id=? and requestor=? and type_r=?',(tr_id,session['user_id'],'C'))
    resp=cur.fetchone()
    if resp[0]==0:          #not yet requested
        r_c='NA'
    else:
        if resp[1]=='NY':
            r_c='NY'
        elif resp[1]=='Y':
            r_c='Y'
        else:
            r_c='N'
    cur.execute('SELECT COUNT(*), response FROM requests WHERE tr_id=? and requestor=? and type_r=?',(tr_id,session['user_id'],'E'))
    resp=cur.fetchone()
    if resp[0]==0:
        r_e='NA'
    else:
        if resp[1]=='NY':
            r_e='NY'
        elif resp[1]=='Y':
            r_e='Y'
        else:
            r_e='N'
    request_data=[r_c,r_e]
    cur.close()
    conn.close()
    notif_count=get_notifs()
    return render_template('post.html',data=data,request_data=request_data, notif_count=notif_count)


@app.route('/request/<int:tr_id>/<type_r>/<int:recipient>/<recipient_name>/<content>/')
@login_required
def req(tr_id,type_r,recipient,recipient_name,content):
    cur,conn=connection()
    cur.execute('CREATE TABLE IF NOT EXISTS requests (request_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, tr_id NUMBER, type_r TEXT, requestor NUMBER, requestor_name TEXT, recipient NUMBER, recipient_name TEXT, response TEXT, ack TEXT, content TEXT)')
    conn.commit()
    cur.execute('INSERT INTO requests (tr_id,type_r,requestor, requestor_name,recipient,recipient_name,response,ack, content) VALUES (?,?,?,?,?,?,?,?,?)',(tr_id,type_r,session['user_id'],session['name'],recipient,recipient_name,'NY','NA',content))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('post',tr_id=tr_id))

@app.route('/remove_post/<int:tr_id>/')
@login_required
def remove_post(tr_id):
    cur,conn=connection()
    cur.execute('DELETE FROM posts WHERE tr_id=?',(tr_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('your_posts'))

@app.route('/notifications/')
@login_required
def notifications():
    cur,conn=connection()
    cur.execute('CREATE TABLE IF NOT EXISTS requests (request_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, tr_id NUMBER, type TEXT, requestor NUMBER, requestor_name TEXT, recipient NUMBER, recipient_name TEXT, response TEXT, ack TEXT, content TEXT)')
    conn.commit()
    cur.execute('CREATE TABLE IF NOT EXISTS help_out (help_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,tr_id NUMBER, helper_id NUMBER, helper_name TEXT, helped_id NUMBER, content TEXT, data_sent TEXT, ack TEXT)')
    conn.commit()
    #recipient_new_notifs
    cur.execute('SELECT * FROM requests WHERE recipient=? AND response=? ORDER BY request_id DESC',(session['user_id'],'NY'))
    recipient_new_notifs=cur.fetchall()
    #recipient_old_notifs
    cur.execute('SELECT * FROM requests WHERE recipient=? AND response=? OR response=? ORDER BY request_id DESC',(session['user_id'],'Y','N'))
    recipient_old_notifs=cur.fetchall()
    #requestor_new_notifs
    cur.execute('SELECT * FROM requests WHERE requestor=? AND ack=? ORDER BY request_id DESC',(session['user_id'],'NS'))
    requestor_new_notifs=cur.fetchall()
    #requestor_old_notifs
    cur.execute('SELECT * FROM requests WHERE requestor=? AND ack=? ORDER BY request_id DESC',(session['user_id'],'S'))
    requestor_old_notifs=cur.fetchall()
    cur.execute('SELECT help_id,helper_name, data_sent,content FROM help_out where helped_id=? AND ack=? ORDER BY help_id DESC',(session['user_id'],'NY'))
    helped_new=cur.fetchall()
    cur.execute('SELECT help_id,helper_name, data_sent,content FROM help_out where helped_id=? AND ack=? ORDER BY help_id DESC',(session['user_id'],'S'))
    helped_old=cur.fetchall()
    cur.close()
    conn.close()
    notif_count=get_notifs()
    return render_template('notifications.html',recipient_new_notifs=recipient_new_notifs,recipient_old_notifs=recipient_old_notifs,requestor_new_notifs=requestor_new_notifs,requestor_old_notifs=requestor_old_notifs,notif_count=notif_count,helped_new=helped_new,helped_old=helped_old)

@app.route('/request/accept/<int:request_id>/')
@login_required
def accept_request(request_id):
    cur,conn=connection()
    cur.execute('UPDATE requests SET response=?,ack=? WHERE request_id=?',('Y','NS',request_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('notifications'))

@app.route('/request/reject/<int:request_id>/')
@login_required
def reject_request(request_id):
    cur,conn=connection()
    cur.execute('UPDATE requests SET response=?,ack=? WHERE request_id=?',('N','NS',request_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('notifications'))

@app.route('/notif/ack/<int:request_id>/')
@login_required
def ack_notif(request_id):
    cur,conn=connection()
    cur.execute('UPDATE requests SET ack=? WHERE request_id=?',('S',request_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('notifications'))

@app.route('/ack_help/<int:help_id>/')
@login_required
def ack_help(help_id):
    cur,conn=connection()
    cur.execute('UPDATE help_out SET ack=? WHERE help_id=?',('S',help_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('notifications'))
@app.route('/logout/')
@login_required
def logout():
    session.clear()
    #flash('You are now logged out')
    return redirect(url_for('index'))

@app.route('/about/')
@login_required
def about():
    notif_count=get_notifs()
    return render_template('about.html',notif_count=notif_count)

@app.errorhandler(404)
def page_not_found(e):

    return render_template('404.html')

@app.errorhandler(500)
def page_not_found(e):

    return render_template('500.html')

@app.route('/admin/',methods=['GET','POST'])
@login_required
def admin():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        sequence=request.form['sequence']
        if name=='XXXXXX' and password=='XXXXXX' and sequence=='XXXXXX':
            session['admin']=True
            return redirect(url_for('board',num=1))
        else:
            error="Fuck off!"
            return render_template('admin.html',notif_count=0,error=error)
    else:
        return render_template('admin.html',notif_count=0)


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin' in session:
            return f(*args,**kwargs)
        else:
            return redirect (url_for('index'))
    return wrap

@app.route('/admin_remove_post/<int:tr_id>/')
@login_required
@admin_required
def admin_remove_post(tr_id):
    cur,conn=connection()
    cur.execute('DELETE FROM posts WHERE tr_id=?',(tr_id,))
    cur.execute('DELETE FROM requests WHERE tr_id=?',(tr_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('board',num=1))

@app.route('/admin/users/')
@login_required
@admin_required
def admin_users():
    cur,conn=connection()
    cur.execute('SELECT user_id,user_name,name,email FROM users ORDER BY user_id DESC')
    data=cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_users.html',data=data,notif_count=0)

@app.route('/admin/remove_user/<int:user_id>/')
@login_required
@admin_required
def admin_remove_user(user_id):
    cur,conn=connection()
    cur.execute('DELETE FROM posts WHERE user_id=?',(user_id,))
    cur.execute('DELETE FROM requests WHERE requestor=?',(user_id,))
    cur.execute('DELETE FROM requests WHERE recipient=?',(user_id,))
    cur.execute('DELETE FROM users WHERE user_id=?',(user_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('admin_users'))


if __name__=="__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True,threaded=True)
