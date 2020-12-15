import sqlite3 

conn=sqlite3.connect("db.db")
c=conn.cursor()


conn.commit()
#c.execute("insert into books values(NULL,'BOBS','BOBS',2,'BOBS','BOBS',1,1,1,'BOBS',12,'BOBS','BOBS','BOBS')")
#c.execute("insert into books values(NULL,'BOBS','BOBS',2,'BOBS','BOBS',1,1,1,'BOBS',12,'BOBS','BOBS','BOBS')")
c.execute("insert into customer values(1,'Dogar','2015-12-17','dogar@gmail.com','Dogars Ville','bobs',0,'1234')")
c.execute("SELECT * FROM customer")

x=c.fetchall()
print(x)




conn.commit()
conn.close()
