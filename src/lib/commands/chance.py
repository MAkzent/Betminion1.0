from src.lib.queries import Database
from src.lib.gamble import Gamble
import globals

def chance():
    db = Database()
    channel = globals.CURRENT_CHANNEL
    user = globals.CURRENT_USER
    g = Gamble(channel)
    points = abs(g.rob_yield(multiplier=1))
    db.add_user([user], channel)
    db.modify_points(user, channel, points)
    print user, points, channel
    if points ==  0:
        resp = "Nothing this time! Try again in a half hour?"
    else:
        resp = "You got {0} cash!".format(points)
    return resp
