import globals
from src.lib.bets import Bets

def outcome(args):
    result = args[0]
    
    if result != "win" and result != "lose":
        return "Sorry, but you didn't specified the outcome. You should write !outcome win/lose"
        
    else:
        globals.LAST_RESULT = result
        globals.BETS_DATA.distribute_profit(result)
        
    return "You have distributed the profit"