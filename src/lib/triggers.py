from datetime import datetime, timedelta
import globals

def trigger_less_than_200_for_all(chan):
    try:
        db = Database()
        channel = chan.lstrip("#")
        str_last_time = db.get_last_time_points_reset(channel)[0]
        if str_last_time:
            now = datetime.utcnow()
            last_time = datetime.strptime(str_last_time, "%Y %m %d %H %M %S")
            if now - last_time >= timedelta(1):
                usernames = db.get_all_usernames(channel)
                print usernames
                
                for username in usernames:
                    print username
                    points = db.get_points(channel, username)[0]
                    if points < 200:
                        db.set_points(channel, username, 200)
                
                strnow = datetime.strftime(datetime.utcnow(), "%Y %m %d %H %M %S")
                db.set_last_time_points_reset(channel, strnow)
                return "Points have been reloaded for users who have less than 200!"
                   
        else:
            strnow = datetime.strftime(datetime.utcnow(), "%Y %m %d %H %M %S")
            db.set_last_time_points_reset(channel, strnow)
    
    except Exception as error:
        print error

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