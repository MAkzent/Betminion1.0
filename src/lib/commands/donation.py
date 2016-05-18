from src.lib.commands.cash import Cash
import src.lib.twitch as twitch
import globals


def donation(args):
    c = Cash()
    user = args[0].lower().lstrip("@")
    amount = args[1]
    try:
        amount = int(float(amount.lstrip("$")))
    except Exception as error:
        print error
        return "Amount has to be a number"
    points = int(amount/10) * 750
    c.modify([user], points)
    thanks_message = "Let's get some ravenLove in the chat for {0}'s ${1} donation!".format(user, amount)
    return "{} cash for {}! {}".format(points, user, thanks_message)
