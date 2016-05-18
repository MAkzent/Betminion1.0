import globals

def pot():
    channel = globals.CURRENT_CHANNEL
    current_pot = 0
    try:
        if globals.channel_info[channel]['gamble']["time"] is not None:
            gamble = globals.channel_info[channel]['gamble']
            current_pot = len(gamble["users"]) * gamble["points"]
        else:
            return "There is no gamble, currently!"
    except Exception as error:
        print error
        return "There is no gamble, currently!"
    return "The current pot is {0}! '!join' in!".format(current_pot)
