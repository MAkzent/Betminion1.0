import globals
from src.lib.bets import Bets
from src.lib.queries import Database
from datetime import datetime

def outcome(args):
    result = args[0]
    
    if result != "win" and result != "lose":
        return "Sorry, but you didn't specified the outcome. You should write !outcome win/lose"
        
    else:
        db = Database()
        channel = globals.CURRENT_CHANNEL
        bets = db.are_bets(channel)[0]
        if not bets:
            bts = Bets()
            bts.distribute_profit(result)
            db.set_last_result(channel, result)
            date = datetime.strftime(datetime.utcnow(), "%Y %m %d %H %M %S")
            #So the outcome won't be used twice for same bets
            db.set_bets_started(channel, date)
        else:
            return "The bets are still going on!"
        
    return "You have distributed the profit"