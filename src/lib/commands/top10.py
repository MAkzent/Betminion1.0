from src.lib.queries import Database
import globals


def top10():
    db = Database()
    channel = globals.CURRENT_CHANNEL
    rank_data = db.get_top10(channel)
    # [(1, u'singlerider', 441, u'ravenbot007'), (2, u'nano_machina', 129, u'ravenbot007')]
    candidates = ", ".join([str(i + 1) + ") " + x[1] + ": " + str(x[2]) for i, x in enumerate(rank_data)])
    resp = "The top 10 cash holders are... " + candidates
    return resp
