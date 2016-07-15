#SoftStepper#

Script for Ableton Live to dynamically find up to 10 loopers and monitor their states on the *Softstep2*. this way one knows easily which state the loopers are in without using the Notebook screen

### about ###

SoftStepper is a Ableton Live Remote script which monitores states of loopers.
It doesn't  actually receive any midi from the *Softstep2* itself, it just reacts on 
changes of loopers in Ableton Live liveset and sends midi to the softstep in order to update its LEDs. 

The script checks the names of looper devices dynamically in the current liveset and when a looper with a name (default) 'ssl1' - 'ssl10' is found, the respective
pad's LED will monitor loooper states. Thus max. 10 loopers can be monitored max.
For instance:
If one drops a looper on a track and hits 'ctrl + r' to rename the device and enters
'ssl3' the third pad of the Softstep will monitor the states of this looper.
If one wants to control the states then the usual midi mapping functionality of live should be used. 
I had some problems to control the looper with the scripting to a satisfactory degree, so I decided to use the usual midimapping for this.


### Installation ###
0. The *SoftStep2* should be in standalone mode. It might work in hosted mode but i haven't tested it. In the SoftStep Editor turn of any LED Feedback for the pads you'd like to be the monitors for the loopers - as the this ableton script will take care about controlling the LEDs :) 

1. download the file by clicking here lefthand on the navigation on 'Download' (next to the small cloud-icon)
The resulting file will be something like 'drival-softstepper-e4f632bcb420.zip'. Unzip the file and put the resulting folder 
in Live s MIDI Remote Scripts directory

**find it on Windows:**
in one of the following locations: 
Program Files\Ableton\Live x.x.x\Resources\MIDI Remote Scripts 
ProgramData\Ableton\Live x\Resources\MIDI Remote Scripts 

**find it on Mac here:**
Go to Applications
find Live.app or Ableton Live x.app
Control-click or right-click and select Show Package Contents
The directory is here Contents/App-Resources/MIDI Remote Scripts  

**2.Live s Preferences** 
In Ableton Live open the preferences
click on tab 'link midi' and set up the softstepper as remotecontrol 
as depicted in the screenshot
note that you should turn also the 'track' and 'remote' ins for the Softstep2 as well
![live_ss_1.jpg](https://bitbucket.org/repo/M8b74b/images/1141864497-live_ss_1.jpg)

Note that the name of the script will be called like the name of the folder you moved to lives remote script folder - thus it'll something like
'drival-softstepper-e4f632bcb420' unless you rename the folder 

**3. start Monitoring (quick start)**
Drop a looper into a track and rename the device 'ssl1' as depicted in the screenshot below.
Now click on the *metronome* -
![reset.jpg](https://bitbucket.org/repo/M8b74b/images/2814138009-reset.jpg)
Doesn't matter if on or off just the change triggers the scanning for new loopers. 
*Note that this is a workaround as constantly watching out for new loopers would be to much I guess. One would have to attach a lot device, name, track - listeners which I thought could be avoid. The chang of the metronome triggers a quick scan across all devices for new loopers*

Note that pad number 0 starts to be solid green?
When you now click on the multipurpose button of the looper you'd see the LED changing states accordingly.
![live_ss_2.jpg](https://bitbucket.org/repo/M8b74b/images/4267606010-live_ss_2.jpg)

4. Midimap as usual
In order to not just monitor the state simply midi-map the a softstep-pad to the multipurpose button of the looper

5. Configuration
Not much to configure but if one wants she can turn on Logging which will write to a logfile 
in the folder of the remotescript. More settings can be found in this file : 'LooperMonitorSettings.py' 

### LED Feedback ###

If the Looper stopped: solid green
If the Looper records: solid red
If the Looper plays: flashing green
If the Looper overdubs: flashing red



### Remember to turn off internal LED of the softstep in the editor ###