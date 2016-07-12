
from LooperMonitorSettings import *

# comment below to disable logging

debug = DEBUG
info = True
error = True
nameOfLogfile = "SoftStepperLog.log"

def log(msg):
	if not debug:
		return
	if not IS_LOGGING_ACTIVE:
		return
	f = open(__file__.replace('.pyc', '.py').replace('Logging.py', nameOfLogfile), 'a')
	label = "[DEBUG] "
	f.write(label + msg+"\n")
	f.close()
	
def log_info(msg):
	if not log_info:
		return
	if not IS_LOGGING_ACTIVE:
		return
	f = open(__file__.replace('.pyc', '.py').replace('Logging.py',nameOfLogfile), 'a')
	label = "[INFO] "
	f.write(label + msg+"\n")
	f.close()
	
def log_error(msg):
	if not log_error:
		return
	if not IS_LOGGING_ACTIVE:
		return
	f = open(__file__.replace('.pyc', '.py').replace('Logging.py',nameOfLogfile), 'a')
	label = "[ERROR] "
	f.write(label + msg+"\n")
	f.close()

def log_warning(msg):
	if not log_error:
		return
	if not IS_LOGGING_ACTIVE:
		return
	f = open(__file__.replace('.pyc', '.py').replace('Logging.py',nameOfLogfile), 'a')
	label = "[WARNING] "
	f.write(label + msg+"\n")
	f.close()
