from src.lib.queries import Database
from datetime import datetime, timedelta
import globals

def claim():
    username = globals.CURRENT_USER
    channel = globals.CURRENT_CHANNEL
    db = Database()
    points = db.get_points(channel, username)[0]
    if points < 200:
        now = datetime.utcnow()
        str = db.get_last_changed_below_200(channel, username)[0]
        last_changed = datetime.strptime(str, "%Y %m %d %H %M %S")
        
        if now - last_changed >= timedelta(1):
            db.set_points(channel, username, 200)
            strnow = datetime.strftime(datetime.utcnow(), "%Y %m %d %H %M %S")
            db.set_last_changed_below_200(channel, username, strnow)
            return "Your points have been reloaded from {0} to 200 points. Points reload once every 24h".format(points)
            
        else:
            return "Sorry, but 24h have not yet passed"
            
    else:
        return "Sorry, but you have more than 200 points"