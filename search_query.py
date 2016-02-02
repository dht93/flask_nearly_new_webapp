import sqlite3

conn=sqlite3.connect('users.sqlite')
cur=conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS search (keyword TEXT, tr_id INTEGER)')
conn.commit()

cur.execute('SELECT tr_id, content FROM posts')
data=cur.fetchall()

for word in data:
    w=word[1].replace(',','').replace('.','').replace('-','').replace('(',' ').replace(')',' ').lower()
    els=w.split(' ')
    for el in els:
        if len(el)>3:
            cur.execute('INSERT INTO search VALUES (?,?)',(el,word[0]))
            conn.commit()
