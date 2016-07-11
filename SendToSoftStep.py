#Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchpad/ConfigurableButtonElement.py
import Live
from _Framework.ButtonElement import *

class SendToSoftStep(ButtonElement):
    """ Special button class for the softste. Im doesn t receive - it is just used to send back to softstep """

    def __init__(self, buttonNum):
        is_momentary = True
        ButtonElement.__init__(self, is_momentary, 1, buttonNum, 20)
        
        self.buttonNum = buttonNum # the button on the softstep
        self._LED_OFF = 0
        self._LED_ON = 1
        self._LED_FAST_FLASH = 2
        self._LED_SLOW_FLASH = 3
        
        # pad 1 is 20, pad 2 = 21
        self._RED_CC_START = 20
        # pad 1 is 110, pad 2 = 21
        self._GREEN_CC_START = 110
        
        self._on_value = 127
        self._off_value = 4
        self._is_enabled = True
        self._is_notifying = False
        self._force_next_value = False
        self._pending_listeners = []
        
        self.ledOffBtn = None
        self.ledRedOnBtn = None
        self.ledRedFastFlashBtn = None
        self.ledRedSlowFlashBtn = None
        
        self.ledGreenOnBtn = None
        self.ledGreenFastFlashBtn = None
        self.ledGreenSlowFlashBtn = None
        
        self.redStateButton = None
        self.greenStateButton = None
        
        self.setup()

    def setup(self):
        self.stateControl = []
        is_momentary = True
        BUTTONCHANNEL = 0 #Channel assignment for all mapped buttons/pads; valid range is 0 to 15
        MESSAGETYPE = 1 #Message type for buttons/pads; set to 0 for MIDI Notes, 1 for CCs.  
        self.redStateButton = ButtonElement(is_momentary, MESSAGETYPE, BUTTONCHANNEL, self._RED_CC_START + self.buttonNum)
        self.greenStateButton = ButtonElement(is_momentary, MESSAGETYPE, BUTTONCHANNEL, self._GREEN_CC_START + self.buttonNum)           

    def off(self):
        self.greenOff()
        self.redOff()
        
    def redOff(self):
        self.redStateButton._do_send_value(self._LED_OFF,0)
        
    def red(self):
        self.greenOff()
        self.redStateButton._do_send_value(self._LED_ON,0)
    
    def orange(self):
        self.greenOff()
        self.redOff() 
        self.greenStateButton._do_send_value(self._LED_ON,0)    
        
    def redFastFlash(self):
        self.greenOff()
        self.redStateButton._do_send_value(self._LED_FAST_FLASH,0)
        
    def redSlowFlash(self,):
        self.greenOff()
        self.redStateButton._do_send_value(self._LED_SLOW_FLASH,0)
        
    def greenOff(self):
        self.greenStateButton._do_send_value(self._LED_OFF,0)
        
    def green(self):
        self.redOff()
        self.greenStateButton._do_send_value(self._LED_ON,0)
        
    def greenFastFlash(self):
        self.redOff()
        self.greenStateButton._do_send_value(self._LED_FAST_FLASH,0)
        
    def greenSlowFlash(self,):
        self.redOff()
        self.greenStateButton._do_send_value(self._LED_SLOW_FLASH,0)
    
 