import globals

def result():
    outcome = globals.LAST_RESULT

    if outcome:
        return "Last outcome was: {0}".format(outcome)
        
    else:
        return "There were no bets yet"