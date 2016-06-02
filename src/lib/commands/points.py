from src.lib.queries import Database
import globals

def points():
    username = globals.CURRENT_USER
    db = Database()
    try:
        points = int(db.get_points(username)[0])
    except Exception as error:
        print error
        return "Couldn't show your points, sorry!"
    return "You have {0} points!".format(points)
