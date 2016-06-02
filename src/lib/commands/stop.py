import globals
from src.lib.betsthread import initialize
from src.lib.queries import Database

def stop():
    channel = globals.CURRENT_CHANNEL
    chan = "#" + channel
    db = Database()
    bets = db.are_bets(channel)[0]
    if bets:
        delay = 3
        initialize(chan, delay)
        
    else:
        return "You haven't started a bet yet!"
    
    return "You have started the countdown"
