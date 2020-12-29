
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
                       #  [0, "ssl1"]
                       # ,[1, "ssl2"]
                       # ,[2, "ssl3"]
                       # ,[3, "ssl4"]
                       [4, "ssl5"]
                       #,[5, "ssl6"]
                       # ,[6, "ssl7"]
                       # ,[7, "ssl8"]
                       # ,[8, "ssl9"]
                       # ,[9, "ssl10"]
                       ]



# Set to 'True' if you want a logfile  
IS_LOGGING_ACTIVE = False

# set to False if logs should show only info stuff
DEBUG = False
