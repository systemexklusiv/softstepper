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
The *SoftStep2* should be in standalone mode. It might work in hosted mode but i haven't tested it. In the SoftStep Editor turn of any LED Feedback for the pads you'd like to be the monitors for the loopers - as the this ableton script will take care about controlling the LEDs :) 

** 1. download the remotescript ** by clicking here lefthand on the navigation on 'Download' (next to the small cloud-icon). In the following screen click on 'download repository'.
The resulting file will be something like 'drival-softstepper-e4f632bcb420.zip'.
** -> Unzip the folder**
** -> rename the folder** *because Live doesnt like dashes in remotescript names* call the folder 
*softstepper* and put the resulting folder in Live s MIDI Remote Scripts directory.

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

Note that the name of the script will be called like the name of the folder you moved to lives remote script folder - thus if you renamed it earlier to *Softstepper* you'll have to look for that name in the drop-down selection


**3. start Monitoring (quick start)**
Drop a looper into a track and rename the device 'ssl1'.
Now click on the *metronome* -
![reset.jpg](https://bitbucket.org/repo/M8b74b/images/2814138009-reset.jpg)
Doesn't matter if on or off just the change triggers the scanning for new loopers. 
*Note that this is a workaround as constantly watching out for new loopers would be to much I guess. One would have to attach a lot device, name, track - listeners which I thought could be avoid. The change of the metronome triggers a quick scan across all devices for new loopers*

After scanning all tracks live recognizes the looper with name 'ssl1'and you should see that pad number 0 starts to be solid green?
When you now click on the multipurpose button of the looper you'd see the LED changing states accordingly.

# one can give a looper-device the follwoing names:
* ssl1 -> pad 1 on softstep2 monitors this looper 
* ssl2 -> pad 2 on softstep2 monitors this looper 
* ssl3 -> pad 3 on softstep2 monitors this looper 
* ssl4 -> pad 4 on softstep2 monitors this looper 
* ssl5 -> pad 5 on softstep2 monitors this looper 
* ssl6 -> pad 6 on softstep2 monitors this looper 
* ssl7 -> pad 7 on softstep2 monitors this looper 
* ssl8 -> pad 8 on softstep2 monitors this looper 
* ssl9 -> pad 9 on softstep2 monitors this looper 
* ssl10 -> pad 10 on softstep2 monitors this looper

### Midimap as usual ###
In order to not just monitor the state simply midi-map the a softstep-pad to the multipurpose button of the looper


### LED Feedback ###

If the Looper stopped: solid green
If the Looper records: solid red
If the Looper plays: flashing green
If the Looper overdubs: flashing red

### Remember to turn off internal LED of the softstep in the editor ###

### 'deeper' configuration ###
Not much to configure but if one wants she can turn on Logging which will write to a logfile 
in the folder of the remotescript. More settings can be found in this file : 'LooperMonitorSettings.py'. It looks like this:

```
#!python
#An monitor assignment consists of:
# a number between 0 and 10 for adressing a LED on the SoftStep2
#and the name which one has to give a Live looper in order to be monitored

# This is where the assignments happen, each assignment is a tupel 
# consisting of a pad, where the feedback will be adressed to
# and a name. The name will be looked up by this scriot for all loopers put into the set.
# if you rename a looper device in your liveact accordingly, 
# the looper states will be mirrored on your softstep

# Below is an example where a looper-device named "ssl" will be monitored on the
# Softstep Pad '1' and anoter looper which will be monitored on pad '5'
# note that the numbers below are zero-based thus 0 menas pad 1
LOOPERS_TO_BE_MONITORED = [
                       [0, "ssl1"]
                       ,[1, "ssl2"]
                       ,[2, "ssl3"]
                       ,[3, "ssl4"]
                       ,[4, "ssl5"]
                       ,[5, "ssl6"]
                       ,[6, "ssl7"]
                       ,[7, "ssl8"]
                       ,[8, "ssl9"]
                       ,[9, "ssl10"]
                       ]



# Set to 'True' if you want a logfile  
IS_LOGGING_ACTIVE = True

# set to False if logs should show only info stuff
DEBUG = True

```