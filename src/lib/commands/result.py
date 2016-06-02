from src.lib.queries import Database
import globals

def result():
    db = Database()
    channel = globals.CURRENT_CHANNEL
    
    try:
        outcome = db.get_last_result(channel)[0]
        return "Last outcome was: {0}".format(outcome)

    except:
        print error
        return "There were no bets yet"