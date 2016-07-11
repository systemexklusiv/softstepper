import Live
from Logging import log as l
from Logging import log_info as i
from Logging import log_error as e
from Logging import log_warning as w

from SendToSoftStep import SendToSoftStep
from LooperMonitorSettings import  *

# Device On * State * Feedback * Reverse * Monitor * Speed * Quantization * Song Control * Tempo Control
class LiveSetObserver():
	__doc__ = " LiveSetObserver "

	# wathces for a device from live with a given nme by a user
	# if something happens 
	def __init__(self, controlsurface, originalDevName, monitors = []):
		self._controlsurface = controlsurface
		self._song = controlsurface.song()
		self.originalDevName = originalDevName

		# The listeners to be informed if certain liveset situation occour
		self._monitors = monitors
		self._song.add_tracks_listener(self.onTracksChanged)
		
		self.setUpListeners()
		
		self.init()
		
	def init(self):
		tracks = self._controlsurface.song().tracks
		l(self.__doc__ + " init")
		for track in tracks:
			self.checkThisTrack(track)

	def addMonitors(self, monitors):
		self._monitors.append(monitors);

	def onTracksChanged(self):
		l(self.__doc__ + "changed amount tracks!")
		self.checkThisTrack(self._song.view.selected_track)
	
	def setUpListeners(self):
		l(self.__doc__ + "Setting up listeners")
		tracks = self._controlsurface.song().tracks
		for track in tracks:
			if track.devices_has_listener(self.onDeviceAdded):
				track.remove_devices_listener(self.onDeviceAdded)
			track.add_devices_listener(self.onDeviceAdded)
			
			for dev in track.devices:
				if dev.class_display_name == self.originalDevName:
					l(self.__doc__ + " setting up bname listener for device with name :" + dev.name)
					if dev.name_has_listener(self.looperNameListener):
						dev.remove_name_listener(self.looperNameListener)
					dev.add_name_listener(self.looperNameListener)
		
	def onDeviceAdded(self):
		selTrack = self._song.view.selected_track
		l(self.__doc__ + " device added/removed on Track " + selTrack.name)
		for dev in selTrack.devices:
			if dev.class_display_name == self.originalDevName:
				l(self.__doc__ +  " a  looper device added! informing monitor listeners!")
				self.checkThisTrack(self._song.view.selected_track)
							
	
	def looperNameListener(self):
		l(self.__doc__ + "looper name changed")
		self.checkThisTrack(self._song.view.selected_track)
	
	def getAllLoopersOfLiveSet(self):
		tracks = self._controlsurface.song().tracks
		toReturn = []
		for track in tracks:
			#if track.has_audio_input:
				for dev in track.devices:
					if dev.class_display_name == self.originalDevName:
						l(self.__doc__ + " found looper with name :" + dev.name)
						toReturn.append(dev)
		return toReturn  
	
	
	def checkThisTrack(self,  track):
		devices = []
		for dev in track.devices:
			if dev.class_display_name == self.originalDevName:
				l(self.__doc__ + " found device with name :" + dev.name)
				devices.append(dev)
		if devices:
			self.informMonitorsWithDevices(devices)
		self.setUpListeners()
		
	
	def informMonitorsWithDevices(self, devices):	
		for monitor in self._monitors:
			l(self.__doc__ + " informing " +str(len(self._monitors)) + " monitors ")
			monitor.checkTheseDevices(devices)
			
		
	def getTrackWithDevice(self, device):
		tracks = self._controlsurface.song().tracks
		for track in tracks:
			#idx = list(track.devices).index(device) if device in track.devices else -1
			if device in track.devices:
				return track
		return None  
