import globals
from datetime import datetime
from src.lib.bets import Bets
from src.lib.queries import Database

def start():
    db = Database()
    channel = globals.CURRENT_CHANNEL
    bets = db.are_bets(channel)[0]
    if not bets:
        chan = "#" + channel
        irc = globals.irc
        
        db.set_bets(channel, 1)
        date = datetime.strftime(datetime.utcnow(), "%Y %m %d %H %M %S")
        db.set_bets_started(channel, date)
        
        msg = "Bets are open! Type !win or !lose with the amount of points you want to bet, example: !win 200"
        irc.send_message(chan, msg)
        return "You have opened the bets"
        
    else:
        return "First, resolve current bets"
