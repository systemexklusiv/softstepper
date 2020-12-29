import Live
from Logging import log as l
from Logging import log_info as i
from Logging import log_error as e
from Logging import log_warning as w

from SendToSoftStep import SendToSoftStep
from LooperMonitorSettings import  *

# Device On * State * Feedback * Reverse * Monitor * Speed * Quantization * Song Control * Tempo Control
class LooperControl():
	__doc__ = " LooperControl "

	def __init__(self, controlsurface, buttonNum, looper_name_to_be_monitored):
		self.P_STATE = "State"
		self.LOOPER_DEV_NAME = "Looper"
		self.looper_name_to_be_monitored = looper_name_to_be_monitored 
		self.LOPPER_STOP = 0.0 
		self.LOPPER_REC = 1.0 
		self.LOPPER_PLAY = 2.0 
		self.LOPPER_OVR = 3.0 
		self.looperToControl = None
		
		self._lcb = None # to be done: a bottun to change the looper states
		self._controlsurface = controlsurface
		self._song = controlsurface.song()
		self._stateButton = SendToSoftStep(buttonNum)
		
		#self.setupLooperControl()
		
		# the current loper which is determined with the id
		self._currentLooperState = self.LOPPER_STOP
		self.offLed()
		
	def offLed(self):
		self._stateButton.off()	
	

	def checkTheseDevices(self, loopers):
		''' central method to call with looper devices
			first the current loopers is set to none
			and in the following new candidates are allocated
		'''
		if loopers:
			candidates = self.getLoopersWithId(loopers)
			if candidates:
				looperToControl = self.getLooperToControl(candidates)
				#if looperToControl is not None and hasattr(looperToControl, '_get_parameters'):
				if looperToControl is not None:
					self.looperToControl = looperToControl
					for param in self.looperToControl.parameters:
						if param.name == self.P_STATE:
							i("Setting up monitor for looper with name: " + self.looper_name_to_be_monitored + " for param " + self.P_STATE)
							self.setupLooperStateListener(param)
							self.sendInitLED()
		else:
			i("There is no looper with name: " + self.looper_name_to_be_monitored + " to be monitored in your liveact!")
			self.offLed()
			self.removeLooperStateListener()
			self.looperToControl = None
	
	#led the looper state decide which init light to send
	def sendInitLED(self):
		if self.looperToControl:
			self.looperValueListener()
		else:
			self.offLed()	
			
	def removeLooperStateListener(self):
		if self.looperToControl is not None:
			for param in self.looperToControl._get_parameters():
						if param.name == self.P_STATE:
							l(__doc__+ " removing state listener from looper: " + self.looperToControl.name)
							if param.value_has_listener(self.looperValueListener):
								param.remove_value_listener(self.looperValueListener)
									
	def setupLooperStateListener(self, param):
		if param is not None:
			if param.value_has_listener(self.looperValueListener):
				param.remove_value_listener(self.looperValueListener)
			param.add_value_listener(self.looperValueListener)	
			
	def looperValueListener(self):
		if self.looperToControl is not None:
			l(self.__doc__ + " looper value listener is notified of state change with name: " + self.looper_name_to_be_monitored)
			for param in self.looperToControl.parameters:
				if param.name == "State":
					l("Looper State changed with val: " + str( param.value))
					
					if param.value == self.LOPPER_STOP:
						self._currentLooperState = self.LOPPER_STOP
						self._stateButton.green()
						
					if param.value == self.LOPPER_REC:
						self._currentLooperState = self.LOPPER_REC
						self._stateButton.red()
						
					if param.value == self.LOPPER_OVR:
						self._currentLooperState = self.LOPPER_OVR
						self._stateButton.redSlowFlash()
						
					if param.value == self.LOPPER_PLAY:
						self._currentLooperState = self.LOPPER_PLAY
						self._stateButton.greenSlowFlash()
		else:
			e(self.__doc__ + "At this point the looperToControl with nae:  must not be None!")				
				
	def getLoopersWithId(self, loopers = None):
		toReturn = []
		allLoopers = loopers
		if not loopers:
			allLoopers = self.getAllLoopersOfLiveSet()	
		if len(allLoopers) > 0:
			for looper in allLoopers:
				l(self.__doc__ + "checking name for id :" + looper.name)
				if looper.name == self.looper_name_to_be_monitored:
					l(self.__doc__ + "found Looper with Id :" + looper.name)
					toReturn.append(looper)
		return toReturn  	
				
	def getLooperToControl(self, looperDevices):	
		l(self.__doc__ + " found num loopers with ids: " + str(len(looperDevices)))
		if looperDevices is not None and len(looperDevices) > 0:
			# check if more than one looper with the expected name are in the liveset
			if len(looperDevices) > 1:
				w("there are more than one custom looper!")
				for looper in looperDevices:
					tr = self.getTrackWithDevice(looper)
					if tr is not None:
						w(self.__doc__ + "found one on track with name: " + tr.name)
					else:
						e(self.__doc__ + " - something went wrong! there must be a track housing " + l.name)
			# take the last appened looper - thus if there are more devices the last appended wins		
			looperToControl = looperDevices[len(looperDevices)-1]
			i("there is a looper found to monitor in liveset with device name: " + self.looper_name_to_be_monitored)
			return looperToControl;
		else:
			i("there is no looper found in liveset with device name: " + self.looper_name_to_be_monitored + "-> make sure you loaded a looper and renamed it");			
		
		
			
	# Device On * State * Feedback * Reverse * Monitor * Speed * Quantization * Song Control * Tempo Control

	def setupSoftStepReceiver(self):
		if self._lcb.value_has_listener(self.onSoftstepPadPressed):
			self._lcb.remove_value_listener(self.onSoftstepPadPressed)
		self._lcb.add_value_listener(self.onSoftstepPadPressed)
		
		#rack_device = device if isinstance(device, Live.RackDevice.RackDevice) else None
	def onSoftstepPadPressed(self, value):
		l("onSoftstepPadPressed")
		assert (value in range(128))
		if value > 0:
			currParam = self.getCurrentStateParam()
			l("onSoftstepPadPressed param name: " + currParam.name)
			l("current state: " + str(currParam))
			l("is enabled: " + str(currParam.is_enabled))
			
			currParam.value = self.LOPPER_REC
# 			if currParam.value == self.LOPPER_STOP:
# 			       currParam.value = self.LOPPER_REC
# 			elif currParam == self.LOPPER_REC:
# 			   	    currParam.value  = self.LOPPER_PLAY				
# 			elif currParam == self.LOPPER_PLAY:
# 				    currParam.value  = self.LOPPER_OVR	
# 			elif currParam.value == self.LOPPER_OVR:
# 					currParam.value  = self.LOPPER_PLAY	
				
	#def setupLooperStateListener(self):
	#	param = self.getCurrentStateParam()
	#	if param is not None:
	#		param.add_value_listener(self.looperValueListener)
	
	def getCurrentStateParam(self):
		looperToControl = self.getLooperToControl()
		if looperToControl is not None:
			for param in looperToControl._get_parameters():
				if param.name == self.P_STATE:
					return param
		else:
			i("There is not looper device to be monitored in your liveact!")
			   
 	
	def getAllLoopersOfLiveSet(self):
		tracks = self._controlsurface.song().tracks
		toReturn = []
		for track in tracks:
			#if track.has_audio_input:
				for dev in track.devices:
					if dev.class_display_name == self.LOOPER_DEV_NAME:
						l(self.__doc__ + " found looper with name :" + dev.name)
						toReturn.append(dev)
		return toReturn  

