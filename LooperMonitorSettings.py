
# An monitor assignment consists of:
# a number between 0 and 10 for adressing a LED on the softstep
#and the name which one has to give a Live looper in order to be monitored


# This is where the assignments happen, each assignment is a tupel 
# consisting of a pad, where the feedback will be adressed to
# and a nam. The name will be looked uo by this scriot in you live act.
# if you rename a looper device in your liveact accordingly, 
# the looper states will be monitored
LOOPERS_TO_BE_MONITORED = (
                           (0, "ssl1" )
                           #,(4, "ssl2" )
                           )
