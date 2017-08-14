# change to python3 if you want to use python3 version
#!/usr/bin/python2

import tornado.ioloop, tornado.web ,tornado.httpserver ,tornado.process ,tornado.template ,tornado.log
import os, sys, traceback, time, argparse, threading

#pretty print
import pprint

#scheduler
import schedule

#db
import sqlite3, json

#gpio
import RPi.GPIO as GPIO, Adafruit_ADS1x15 

#argument check


#config
web_server_port = 8080
html_page_path = dir_path = os.path.dirname(os.path.realpath(__file__)) + '/www/'
#html_page_path = dir_path = web_doc_root

# check a bit is hi or low
def check_bit(value=0,bit_num=0):
	return ((value & (1<<bit_num))>>bit_num)
	
# db class
class DBFeeder(object):
	def __init__(self,dbname='feeder.db'):
		try:
			self.dbname = dbname
			self.con = sqlite3.connect(self.dbname)
			self.init_success = True
		except:
			pass
			self.init_success = False
			
	def close(self):
		try:
			self.con.close()
		except:
			pass
			
	def get_schedule_list(self, in_json = False):
		try:
			if self.init_success:
				self.con.row_factory = sqlite3.Row
				cur = self.con.cursor()
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

# feeder system class
class Feeder(object):
	def __init__(self):
		# adc gp2y init
		self.GP2Y_ADC = None

		# global variable
		self.PWM_SERVO = None
		
	# setup the gpio
	def gpio_setup(self):
		try:
			GPIO.setwarnings(False)
			GPIO.setmode(GPIO.BOARD)
			
			# setup pwm pin
			GPIO.setup(7,GPIO.OUT)
			self.PWM_SERVO=GPIO.PWM(7,50)
			self.PWM_SERVO.start(7.5)
			
			# setup motor pin
			GPIO.setup(13,GPIO.OUT)
			GPIO.output(13,GPIO.LOW)
			
			# init adc
			self.GP2Y_ADC = Adafruit_ADS1x15.ADS1115()
			
			return (0,'')
		except:
			pass
			return (1,sys.exc_info()[1])

	# cleanup gpio
	def gpio_cleanup(self):
		try:
			GPIO.cleanup()
		except:
			pass
			
	# baca sensor gp2y
	def gp2y_read(self):
		try:
			value = self.GP2Y_ADC.read_adc(0)
			cm = (1.0 / ((value/5890.90) / 15.7)) - 0.42
			persen=0
			if cm > 32:
				persen=0
			elif cm > 26.5:
				persen=25
			elif cm > 15.5:
				persen=50
			elif cm > 10:
				persen=75
			elif cm < 10:
				persen=100
			return (cm,persen)
		except:
			pass
			return (-1,0)
	
	# motor on off
	def motor_on_off(self, isOn=False):
		# GPIO.output(13,isOn ? GPIO.HIGH:GPIO.LOW)
		GPIO.output(13, isOn * GPIO.HIGH)
		
	# servo on off
	def servo_on_off(self):
		try:
			self.PWM_SERVO.ChangeDutyCycle(4.5)
			time.sleep(3)
			self.PWM_SERVO.ChangeDutyCycle(6.5)
			time.sleep(6)
			self.PWM_SERVO.ChangeDutyCycle(4.5)
			time.sleep(3)
			self.PWM_SERVO.ChangeDutyCycle(6.5)
			time.sleep(6)
			self.PWM_SERVO.ChangeDutyCycle(4.5)
			time.sleep(3)
			self.PWM_SERVO.ChangeDutyCycle(6.5)
			time.sleep(6)
			self.PWM_SERVO.ChangeDutyCycle(4.5)
			time.sleep(3)
			self.PWM_SERVO.ChangeDutyCycle(6.5)
			time.sleep(6)
			self.PWM_SERVO.ChangeDutyCycle(4.5)
			time.sleep(3)
			self.PWM_SERVO.ChangeDutyCycle(6.5)
			time.sleep(6)
			self.PWM_SERVO.ChangeDutyCycle(4.5)
			time.sleep(3)
			self.PWM_SERVO.ChangeDutyCycle(6.5)
			time.sleep(6)
			self.PWM_SERVO.ChangeDutyCycle(4.5)
			time.sleep(3)
			self.PWM_SERVO.ChangeDutyCycle(6.5)
			time.sleep(6)
			self.PWM_SERVO.ChangeDutyCycle(4.5)
			time.sleep(3)
			self.PWM_SERVO.ChangeDutyCycle(6.5)
			time.sleep(6)
			self.PWM_SERVO.ChangeDutyCycle(4.5)
			time.sleep(3)
			self.PWM_SERVO.ChangeDutyCycle(6.5)
			time.sleep(6)
			self.PWM_SERVO.ChangeDutyCycle(4.5)
			time.sleep(3)
			self.PWM_SERVO.ChangeDutyCycle(6.5)
			time.sleep(6)
			self.PWM_SERVO.ChangeDutyCycle(4.5)
			time.sleep(3)
			self.PWM_SERVO.stop()
			return True
		except:
			return False
			pass
		
	# feed 1kg
	def feed_0_5kg(self, total_feed=0.0):
		ret = 0
		try:
			if self.gp2y_read()[1] > 0:
				if total_feed > 0:
					curr_total = 0.0
					while curr_total <= total_feed:
						if self.gp2y_read()[1] > 0:
							motor_on_off(True)
							servo_on_off()
							time.sleep(2)
							motor_on_off(False)
							curr_total += 0.5
							ret = 0
						else:
							ret = 4
							break
				else:
					ret = 3
			else:
				ret = 2
		except:
			pass
			ret = 1
		
		return ret
	
'''
disable static page cache
'''
class MyStaticFileHandler(tornado.web.StaticFileHandler):
	def set_extra_headers(self, path):
		# Disable cache
		self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')

'''
html page handlers
'''
class HtmlPageHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self, file_name='index.html'):
		# Check if page exists
		index_page = os.path.join(html_page_path, file_name)
		
		# disable cache
		# Set http header fields
		self.set_header('Cache-Control','no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0')
		
		if os.path.exists(index_page):
			# Render it
			#self.render('www/' + file_name)
			self.render(html_page_path + file_name)
		else:
			# Page not found, generate template
			err_tmpl = tornado.template.Template("<html> Err 404, Page {{ name }} not found</html>")
			err_html = err_tmpl.generate(name=file_name)
			# Send response
			self.finish(err_html)
			
class WebApiHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		#process command
		try:
			# get args from GET request
			cmd = int(self.get_argument('c'))
			
			# process the cmd
			# updating
			if cmd == 1:
				id_sch = int(self.get_argument('i'))
				day_on_and_active = int(self.get_argument('d'))
				jam_on = self.get_argument('j')
				brt = float(self.get_argument('w'))
				
				tornado.log.app_log.info('Updating with %d -- %d -- %s -- %f' % (id_sch, day_on_and_active, jam_on, brt))
				
				#print(check_bit(day_on_and_active,7))		
				rowx = dbx.update_schedule(id=id_sch,aktif=check_bit(day_on_and_active,7),senin=check_bit(day_on_and_active,0),selasa=check_bit(day_on_and_active,1),rabu=check_bit(day_on_and_active,2),kamis=check_bit(day_on_and_active,3),jumat=check_bit(day_on_and_active,4),sabtu=check_bit(day_on_and_active,5),minggu=check_bit(day_on_and_active,6),jam=jam_on,berat=brt)
				self.write({'error': 0, 'row': rowx})
				
				tornado.log.app_log.info('Update OK (%d)' % (rowx))
				
			# get schedule
			# http://code.runnable.com/Us3hW_JG2iNMAADr/tornado-server-example-with-sqlite-for-python
			# http://www.cdotson.com/2014/06/generating-json-documents-from-sqlite-databases-in-python/
			# https://stackoverflow.com/questions/3286525/return-sql-table-as-json-in-python
			elif cmd == 2:
				tornado.log.app_log.info('Get schedule list')
				self.write({'error': 0,'data': json.loads(dbx.get_schedule_list(True))})
				
			#reinit schedule
			elif cmd == 3:
				tornado.log.app_log.info('Reinit schedule list')
				scheduler_feeder.init_jobs()
				self.write({'error': 0})
				
			#check pakan
			elif cmd == 4:
				tornado.log.app_log.info('Read feeder level')
				self.write({'error': 0, 'level': fish_feeder.gp2y_read()[1]})
				
			# others
			else:
				tornado.log.app_log.info('Command unknown')
				self.write({'error': 1})			
			
		except:
			self.write({'error': 255})
			
		#always flush and finish it
		self.flush()
		self.finish()

'''
web server handlers
'''
def make_app():
	# add handlers
	return tornado.web.Application([
		#root handlers
		(r'/', HtmlPageHandler),
		(r'/(?P<file_name>[^\/]+htm[l]?)+', HtmlPageHandler),
		(r'/api', WebApiHandler),
		(r'/(?:image)/(.*)', tornado.web.StaticFileHandler, {'path': html_page_path + 'image'}),
		(r'/(?:css)/(.*)', tornado.web.StaticFileHandler, {'path': html_page_path + 'css'}),
		(r'/(?:js)/(.*)', tornado.web.StaticFileHandler, {'path': html_page_path + 'js'}),
		(r'/(?:fonts)/(.*)', tornado.web.StaticFileHandler, {'path': html_page_path + 'fonts'})
		],
	)
	
'''
parse command options
https://gist.github.com/redja/9276216
'''	
def get_args():
	try:
		# Assign description to the help doc
		parser = argparse.ArgumentParser(description='Fish feeder system')
		# Add arguments
		parser.add_argument('-r', '--root', type=str, help='Absolute web server document root path', required=True)
		parser.add_argument('-p', '--port', type=int, help='Web server port number', required=False, default=8080)
		
		# Array for all arguments passed to script
		args = parser.parse_args()
		# Assign args to variables
		root_path = args.root
		server_port = args.port
		# Return all variable values
		return (1, root_path, server_port)
	except:
		pass
		return (0,'','')
		
class FeederSchedulerThread(threading.Thread):
	def __init__(self, name='Feeder Schedule Thread', db_obj=None, feeder_obj=None):
		""" constructor, setting initial variables """
		self._stopevent = threading.Event()
		self._sleepperiod = 1.0
		self._db_obj = db_obj
		self._feeder_obj = feeder_obj
		threading.Thread.__init__(self, name=name)
		
	def run(self):
		""" main control loop """
		tornado.log.app_log.info("%s starts" % (self.getName()))
		
		while not self._stopevent.isSet():
			schedule.run_pending()
			self._stopevent.wait(self._sleepperiod)
			
		tornado.log.app_log.info("%s ends" % (self.getName()))
		
	def stop(self, timeout=None):
		""" Stop the thread and wait for it to end. """
		self._stopevent.set()
		threading.Thread.join(self, timeout)
		
	def get_jobs(self):
		schx = self._db_obj.get_schedule_list()
		for item in schx:
			print(item)
		
	def init_jobs(self):
		try:
			#schedule.every(5).seconds.do(self.job)
			#clear all jobs
			schedule.clear()
			schx = self._db_obj.get_schedule_list()
			
			#dummy job per 5 seconds
			schedule.every(5).seconds.do(self.job, id=-1, berat=-1)
			
			for item in schx:
				#got any aktif schedule
				if (item['aktif'] == 1) and (item['berat'] > 0):
					idx = item['id']
					brtx = item['berat']
					jamx = ":".join(item['jam'].split(':')[:2])
					
					tornado.log.app_log.info('Schedule #%d aktif' % (idx))
					
					#scheduling on day on				
					if item['senin'] == 1:
						schedule.every().monday.at(jamx).do(self.job, id=idx, berat=brtx)
					if item['selasa'] == 1:
						schedule.every().tuesday.at(jamx).do(self.job, id=idx, berat=brtx)
					if item['rabu'] == 1:
						schedule.every().wednesday.at(jamx).do(self.job, id=idx, berat=brtx)
					if item['kamis'] == 1:
						schedule.every().thursday.at(jamx).do(self.job, id=idx, berat=brtx)
					if item['jumat'] == 1:
						schedule.every().friday.at(jamx).do(self.job, id=idx, berat=brtx)
					if item['sabtu'] == 1:
						schedule.every().saturday.at(jamx).do(self.job, id=idx, berat=brtx)
					if item['minggu'] == 1:
						schedule.every().sunday.at(jamx).do(self.job, id=idx, berat=brtx)
			
			tornado.log.app_log.info('All active schedule registered')
			pprint.pprint(schedule.jobs)
			#tornado.log.app_log.info(json.dumps(schedule.jobs, indent=4, sort_keys=True))
		except:
			pass
			tornado.log.app_log.error('Cannot reinit all schedule!!!')
		
	def job(self, id=None, berat=0.0):
		try:
			if id == -1:
				tornado.log.app_log.info("Schedule is alive...")
			else:
				tornado.log.app_log.info("Doing job #%d" % (id))
			if id != -1 and id is not None:
				tornado.log.app_log.info("Feeding %f kg" % (berat))
				if self._feeder_obj is not None:
					tornado.log.app_log.info("Feeding starting...")
					retc = self._feeder_obj.feed_0_5kg(total_feed=berat)
					tornado.log.app_log.info("Feeding finish with error code = %d" % (retc))
				else:
					tornado.log.app_log.error("No feeder defined!!!")
		except:
			pass
			tornado.log.app_log.error("Error occured!!!")
				
if __name__ == "__main__":
	try:			
		#process argument
		sts, dir_path, web_server_port = get_args()
		
		#argument valid?
		if(sts==1):
			try:
				html_page_path = dir_path
				
				#init db
				dbx = DBFeeder()
				
				# bind server on 8080 port
				tornado.log.enable_pretty_logging()
				tornado.log.app_log.info('FISH FEEDER on port %d with root at %s initializing...' % (web_server_port,dir_path))	
				
				sockets = tornado.netutil.bind_sockets(web_server_port)
				server = tornado.httpserver.HTTPServer(make_app())
				server.add_sockets(sockets)
				
				tornado.log.app_log.info('Web server initialization success')
				
				# gpio setup
				fish_feeder = Feeder()
				gpio_sts = fish_feeder.gpio_setup()
				if (gpio_sts[0] == 0):
					tornado.log.app_log.info('GPIO init OK')
				else:
					tornado.log.app_log.error('GPIO init ERROR : %s' % (gpio_sts[1]))
				
				# run scheduler
				scheduler_feeder = FeederSchedulerThread(db_obj=dbx, feeder_obj=fish_feeder)
				scheduler_feeder.init_jobs()
				scheduler_feeder.start()
		
				# start tornado thread loop
				tornado.log.app_log.info('Web server loop started')
				tornado.ioloop.IOLoop.current().start()
		
			#except Exception as errx:
			except:
				pass
			#	print(errx)
				print('\n')
				scheduler_feeder.stop()
				tornado.log.app_log.error('Bye...')

			#cleanup
			try:
				dbx.close()
				fish_feeder.gpio_cleanup()
			except:
				pass
	except:
		pass
