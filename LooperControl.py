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
		
		self._lcb = None # to be done: a bottun to change the looper states
		self._controlsurface = controlsurface
		self._song = controlsurface.song()
		self._stateButton = SendToSoftStep(buttonNum)
		
		self.setupLooperControl()
		
		# the current loper which is determined with the id
		self._currentLooperState = self.LOPPER_STOP
		
		self._song.add_tracks_listener(self.onTracksChanged)
		



	def onTracksChanged(self):
		l(self.__doc__ + " changed amount tracks!")
		self.setupLooperControl()
		
			
	# Device On * State * Feedback * Reverse * Monitor * Speed * Quantization * Song Control * Tempo Control
	def setupLooperControl(self):
		self.setupLooperStateListener()
		self.setUpDeviceListner()
		self.setNameListenersToAllLoopers()
		#if self._lcb is not None:
		#	self.setupSoftStepReceiver()


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

			
					
	def setupLooperStateListener(self):
		param = self.getCurrentStateParam()
		if param is not None:
			param.add_value_listener(self.looperValueListener)
	
	def getCurrentStateParam(self):
		looperToControl = self.getLooperToControl()
		if looperToControl is not None:
			for param in looperToControl._get_parameters():
				if param.name == self.P_STATE:
					return param
		else:
			i("There is not looper device to be monitored in your liveact!")
	
	def getLooperToControl(self):
		loopers = self.getLoopersWithId()
		l(self.__doc__ + " found num loopers with ids: " + str(len(loopers)))
		if loopers is not None and len(loopers) > 0:
			# check if more than one looper with the expected name are in the liveset
			if len(loopers) > 1:
				w("there are more than one custom looper!")
				for looper in loopers:
					tr = self.getTrackWithDevice(looper)
					if tr is not None:
						w(self.__doc__ + "found on track with name: " + tr.name)
					else:
						e(self.__doc__ + " - something went wrong! there must be a track housing " + l.name)
			# remove listeners firsthand
			for  looper in loopers:
				for param in looper._get_parameters():
					if param.name == self.P_STATE:
						if param.value_has_listener(self.looperValueListener):
							param.remove_value_listener(self.looperValueListener)
			# take the last appened looper - thus if there are more devices the last appended wins		
			looperToControl = loopers[len(loopers)-1]
			i("there is a looper found to monitor in liveset with device name: " + self.looper_name_to_be_monitored)
			return looperToControl;
		else:
			i("there is no looper found in liveset with device name: " + self.looper_name_to_be_monitored + "-> make sure you loaded a looper and renamed it");
	
	def setUpDeviceListner(self):
		tracks = self._controlsurface.song().tracks
		for track in tracks:
			if track.devices_has_listener(self.onDeviceAdded):
				track.remove_devices_listener(self.onDeviceAdded)
			track.add_devices_listener(self.onDeviceAdded)
	
	def onDeviceAdded(self):
		selTrack = self._song.view.selected_track
		l("device added on Track " + selTrack.name)
		for dev in selTrack.devices:
			if dev.class_display_name == self.LOOPER_DEV_NAME:
				if dev.name == self.looper_name_to_be_monitored:
					l("re-init looper state listeners")
					self.setupLooperControl()
		
	# Here the updates happens				
	def looperValueListener(self):
		loopers = self.getLoopersWithId()
		if len(loopers) > 0:
			looperToControl = loopers[len(loopers)-1]
			l("LooperControl. Detected loopers with id: " + self.looper_name_to_be_monitored + " " + str (len (loopers)))
			for param in looperToControl._get_parameters():
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
					
		
	def getLoopersWithId(self):
		toReturn = []
		allLoopers = self.getAllLoopersOfLiveSet()
		if len(allLoopers) > 0:
			for looper in allLoopers:
				l(self.__doc__ + "checking name for id :" + looper.name)
				if looper.name == self.looper_name_to_be_monitored:
					toReturn.append(looper)
		return toReturn  	
	
	
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
	
	def setNameListenersToAllLoopers(self):
		tracks = self._controlsurface.song().tracks
		loopers = self.getAllLoopersOfLiveSet()
		for looper in loopers:
			if looper.name_has_listener(self.looperNameListener):
				looper.remove_name_listener(self.looperNameListener)
			looper.add_name_listener(self.looperNameListener) 
	
	def looperNameListener(self):
		l(self.__doc__ + " looperNameListener called")
		self.setupLooperControl()
	
	def getTrackWithDevice(self, device):
		tracks = self._controlsurface.song().tracks
		for track in tracks:
			#idx = list(track.devices).index(device) if device in track.devices else -1
			if device in track.devices:
				return track
		return None  
	# boworred from clyphX below, just to taek a look how its done
# 	def get_looper(self, track):
# 	""" Get first looper device on track and its params """
# 	self._looper_data = {}
# 	for d in track.devices:
# 		if d.class_name == 'Looper':
# 		self._looper_data['Looper'] = d
# 		for p in d.parameters: 
# 			if p.name in ('Device On', 'Reverse', 'State'):
# 			self._looper_data[p.name] = p
# 		break
# 		elif not self._looper_data and self._parent._can_have_nested_devices and d.can_have_chains and d.chains:
# 		for c in d.chains:
# 			self.get_looper(c)

	# Live.Track.Track.add_devices_listener()
	# Live.Song.Song.add_tracks_listener()
	#Live.Device.Device.add_name_listener()
	#Live.Device.DeviceType.audio_effect