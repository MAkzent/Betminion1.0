import globals
from src.lib.bets import Bets

def start():

    if not global.BETS:
        channel = globals.CURRENT_CHANNEL
        chan = "#" + channel
        irc = globals.irc
        
        globals.BETS = True
        globals.BETS_DATA = Bets()
        
        msg = "Bets are open! Type !win or !lose with the amount of points you want to bet, example: !win 200"
        irc.send_message(chan, msg)
        return "You have opened the bets"
        
    else:
        return "First, resolve current bets"
