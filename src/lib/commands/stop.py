import globals
from src.lib.betsthread import initialize

def stop():
    channel = globals.CURRENT_CHANNEL
    chan = "#" + channel
    # irc = globals.irc
    if globals.BETS:
        delay = 30
        initialize(chan, delay)
        
    else:
        return "You haven't started a bet yet!"
    
    # msg = "Bets will close in {0} seconds!".format(delay)
    # self.irc.send_message(self.channel, msg)
    return "You have started the countdown"
