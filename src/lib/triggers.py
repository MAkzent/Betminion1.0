import globals

def trigger_less_than_200(username, channel, current_points):
    pass

def trigger_more_than_5000(username, channel, last_points, current_points):
    if last_points < 5000 and current_points >= 5000:
        chan = "#" + channel
        irc = globals.irc
        msg = "/w {0} Feelsgoodman, you're going strong! We'll soon launch our website to trade your points into RP. Keep on winning!".format(username)
        irc.send_message(chan, msg)        