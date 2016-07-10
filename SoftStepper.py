# http://systemexklsuiv.net

from __future__ import with_statement

import Live
from Logging import log as l
from Logging import log_info as i
from Logging import log_error as e
from _Framework.ControlSurface import ControlSurface
from LooperControl import LooperControl
from LooperMonitorSettings import  *

from MIDI_Map import *

class SoftStepper(ControlSurface):
	__doc__ = " Script for SoftStep2 "

	def __init__(self, c_instance):
		ControlSurface.__init__(self, c_instance)
		#self.set_suppress_rebuild_requests(True)
		with self.component_guard():
			self.looperMonitors = []
#			self.lc = LooperControl(self, MONITOR_PAD_NUMBER, LOOPER_NAME_TO_BE_MONITORED_BY_SOFTSTEP)
			i("found number of monitor setups: " + str(len(LOOPERS_TO_BE_MONITORED)))
			for assignment in LOOPERS_TO_BE_MONITORED:
				softStepPadNum = assignment[0]
				looperNameToBeMonitored = assignment[1]
				self.looperMonitors.append(LooperControl(self, softStepPadNum, looperNameToBeMonitored))
			
			i('-----------------------') 	
			i('initialized SoftStepper by systemexklusiv.net')	
			i('-----------------------') 



	  