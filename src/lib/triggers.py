from datetime import datetime, timedelta
import globals
import os
import csv

def trigger_less_than_200_for_all(chan):
    try:
        db = Database()
        channel = chan.lstrip("#")
        str_last_time = db.get_last_time_points_reset(channel)[0]
        if str_last_time:
            now = datetime.utcnow()
            last_time = datetime.strptime(str_last_time, "%Y %m %d %H %M %S")
            if now - last_time >= timedelta(1):
                usernames = db.get_all_usernames()
                
                for username in usernames:
                    points = db.get_points(username)[0]
                    if points < 200:
                        db.set_points(username, 200)
                
                strnow = datetime.strftime(datetime.utcnow(), "%Y %m %d %H %M %S")
                db.set_last_time_points_reset(channel, strnow)
                return "Points have been reloaded for users who have less than 200!"
                   
        else:
            strnow = datetime.strftime(datetime.utcnow(), "%Y %m %d %H %M %S")
            db.set_last_time_points_reset(channel, strnow)
    
    except Exception as error:
        print error

# def trigger_less_than_200(username, channel):
    # db = Database()
    # points = db.get_points(channel, username)[0]
    # if points < 200:
        # irc = globals.irc
        # chan = "#" + channel
        # now = datetime.datetime.utcnow()
        # str = db.get_last_changed_below_200(channel, username)[0]
        # last_changed = datetime.datetime.strptime(str, "%Y %m %d %H %M %S")
        # if now - last_changed >= datetime.timedelta(1):
            # db.set_points(channel, username, 200)
            # strnow = datetime.datetime.strftime(datetime.datetime.utcnow(), "%Y %m %d %H %M %S")
            # db.set_last_changed_below_200(channel, username, strnow)
            # msg = "/w {0} Your points have been reloaded from {1} to 200 points. Points reload once every 24h".format(username, points)
            # irc.send_message(chan, msg)            

def trigger_more_than_5000(username, last_points, points):
    chan = "#" + globals.CURRENT_CHANNEL
    if last_points < 5000 and last_points + points >= 5000:
        irc = globals.irc
        msg = "/w {0} Feelsgoodman, you're going strong! We'll soon launch our website to trade your points into RP. Keep on winning!".format(username)
        irc.send_message(chan, msg)
        
def trigger_clear_bets(chan):
    db = Database()
    bets_data = db.get_all_bets_data()
    
    try:
        #Get the oldest date
        oldest_date = datetime.strptime(bets_data[0][5], "%Y %m %d %H %M %S")
        now = datetime.utcnow()
        if now - oldest_date >= timedelta(30):
            if not os.path.exists(os.path.join('dump')):
                os.makedirs(os.path.join('dump'))
            path = os.path.join("dump", "bets_data_" + datetime.strftime(now, "%Y_%m_%d_%H_%M_%S") + ".csv")
            with open(path, 'wb') as outfile:
                wr = csv.writer(outfile)
                header = ("id", "channel", "username", "amount", "outcome", "date")
                wr.writerow(header)
                for row in bets_data:
                    wr.writerow(row)
            db.clear_bets()
            
    except Exception as error:
        print error
        
from src.lib.queries import Database