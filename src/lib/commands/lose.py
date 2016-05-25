import globals
from src.lib.bets import Bets
from src.lib.queries import Database

def lose(args):
    if globals.BETS:
        username = globals.CURRENT_USER
        channel = globals.CURRENT_CHANNEL
        db = Database()
        
        if db.get_user(username, channel) == None:
            db.add_user([username], channel)
            db.modify_points(username, channel, 1000)
            
        current_points = db.get_points(channel, username)[0]
        
        if (args[0][-1] == "%"):
            try:
                percentage = int(args[0].strip("%"))
            except Exception as error:
                print error
                return "Sorry, but your betting amount should be a number or a percentage"
            if percentage > 100:
                return "Sorry, but you can't bet more than a 100%"
            else:
                multiply = percentage / 100
                amount = int(current_points * multiply)
           
        else:
            try:
               amount = int(args[0])
            except Exception as error:
                print error
                return "Sorry, but your betting amount should be a number or a percentage"
            if amount > current_points:
                return "You currently have {0} points, use them wisely.".format(current_points)
        
        globals.BETS_DATA.add_bidder(username, amount, "lose")
        db.modify_points(username, channel, -amount)
        return "Bet successfully placed! You bet {0} that {1} will lose".format(amount, channel)
        
    else:
        return "Sorry, bets were not started yet"