import MySQLdb

conn=MySQLdb.connect('dht93.mysql.pythonanywhere-services.com','dht93','databasebitches93','dht93$users')
cur=conn.cursor()

cur.execute('INSERT INTO users VALUES (%s,%s)',(3,'daddy_yoyo'))
conn.commit()
print ("done!")