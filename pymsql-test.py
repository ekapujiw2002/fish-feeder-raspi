# change to python3 if you want to use python3 version
#!/usr/bin/python2

#pretty print
import pprint

#db
import pymysql, json

# db class
class DBFeeder(object):
	def __init__(self, driver='mysql', hostname='localhost', username='admin_db', password='1234', dbname='raspi-fish-feeder'):
		try:
			self.type = driver
			self.dbname = dbname
			
			if self.type == 'sqlite':
				self.con = sqlite3.connect(self.dbname)
				
			if self.type == 'mysql':
				self.con = pymysql.connect(hostname,username,password,dbname)
			
			self.init_success = True
		except:
			pass
			self.init_success = False
		   
	def close(self):
		try:
			#if self.type == 'sqlite':
			self.con.close()
				
			#if self.type == 'mysql':
			#	self.con.close()
		except:
			pass
		   
	def get_schedule_list(self, in_json = False):
		try:			
			if self.init_success:
				if self.type == 'sqlite':
					self.con.row_factory = sqlite3.Row
					cur = self.con.cursor()					
					
				if self.type == 'mysql':
					#https://stackoverflow.com/questions/4940670/pymysql-fetchall-results-as-dictionary
					cur = self.con.cursor(pymysql.cursors.DictCursor)
				
				cur.execute('SELECT * FROM feed_schedule ORDER BY id')
				rows = cur.fetchall()
					
				if in_json:
					return json.dumps([dict(ix) for ix in rows])
				return [dict(ix) for ix in rows]
			return None
		except:
			pass
			return None		
	#https://stackoverflow.com/questions/21986194/how-to-pass-dictionary-items-as-function-arguments-in-python
	def update_schedule(self, id=None, aktif=0, senin=0, selasa=0, rabu=0, kamis=0, jumat=0, sabtu=0, minggu=0, jam='00:00:00', berat=0.0):
		try:
			if self.init_success and (id is not None):
				cur = self.con.cursor()
				cur.execute('update feed_schedule set aktif=?, senin=?, selasa=?, rabu=?, kamis=?, jumat=?, sabtu=?, minggu=?, jam=?, berat=? where id=?',(aktif, senin, selasa, rabu, kamis, jumat, sabtu, minggu, jam, berat, id))
				self.con.commit()
				return cur.rowcount
			return 0
		except:
			pass
			return 0

'''
# Open database connection
db = pymysql.connect("localhost","admin_db","1234","raspi-fish-feeder" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()

print ("Database version : %s " % data)

# disconnect from server
db.close()
'''

#init db
dbx = DBFeeder(hostname='localhost',username='admin_db',password='1234',dbname='raspi-fish-feeder')
pprint.pprint(dbx.get_schedule_list())	
dbx.close()	