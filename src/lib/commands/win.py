import globals
from src.lib.bets import Bets
from src.lib.queries import Database
from datetime import datetime

def win(args):
    db = Database()
    channel = globals.CURRENT_CHANNEL
    bets = db.are_bets(channel)[0]
    
    if bets:
        username = globals.CURRENT_USER
        
        if db.get_user(username) == None:
            db.add_user([username])
            db.modify_points(username, 1000)
        
        current_points = db.get_points(username)[0]
        
        if (args[0][-1] == "%"):
            try:
                percentage = int(args[0].strip("%"))
            except Exception as error:
                print error
                return "Sorry, but your betting amount should be a number or a percentage"
            if percentage > 100:
                return "Sorry, but you can't bet more than a 100%"
            else:
                multiply = float(percentage) / 100
                amount = int(current_points * multiply)
           
        else:
            try:
               amount = int(args[0])
            except Exception as error:
                print error
                return "Sorry, but your betting amount should be a number or a percentage"
            if amount > current_points:
                return "You currently have {0} points, use them wisely.".format(current_points)
        
        date = datetime.strftime(datetime.utcnow(), "%Y %m %d %H %M %S") 
        db.add_bidder(channel, username, amount, "win", date)
        db.modify_points(username, -amount)
        return "Bet successfully placed! You bet {0} that {1} will win".format(amount, channel)
        
    else:
        return "Sorry, bets were not started yet"