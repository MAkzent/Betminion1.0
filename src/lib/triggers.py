from datetime import datetime, timedelta
import globals

def trigger_less_than_200(username, channel):
    db = Database()
    points = db.get_points(channel, username)[0]
    if points < 200:
        irc = globals.irc
        chan = "#" + channel
        now = datetime.utcnow()
        str = db.get_last_changed_below_200(channel, username)[0]
        last_changed = datetime.strptime(str, "%Y %m %d %H %M %S")
        if now - last_changed >= timedelta(1):
            db.set_points(channel, username, 200)
            strnow = datetime.strftime(datetime.utcnow(), "%Y %m %d %H %M %S")
            db.set_last_changed_below_200(channel, username, strnow)
            msg = "/w {0} Your points have been reloaded from {1} to 200 points. Points reload once every 24h".format(username, points)
            irc.send_message(chan, msg)            

def trigger_more_than_5000(username, channel, last_points, points):
    print last_points
    if last_points < 5000 and last_points + points >= 5000:
        chan = "#" + channel
        irc = globals.irc
        msg = "/w {0} Feelsgoodman, you're going strong! We'll soon launch our website to trade your points into RP. Keep on winning!".format(username)
        irc.send_message(chan, msg)
        
        
from src.lib.queries import Database