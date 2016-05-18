from src.lib.queries import Database
import globals


def gift(args):
    user = globals.CURRENT_USER
    recipient = args[0].lower().lstrip("@")
    channel = globals.CURRENT_CHANNEL
    try:
        amount = abs(int(args[1]))
    except:
        return "Amount has to be a number!"
    if recipient == user:
        return "You can't gift yourself cash!"
    db = Database()
    if db.get_user(user, channel):
        if db.get_user(user, channel)[2] >= amount and db.get_user(
                recipient, channel):
            db.modify_points(recipient, channel, amount)
            db.modify_points(user, channel, amount * -1)
            return "{0} cash has been debited to {1}!".format(amount, recipient)
        else:
            return "Those numbers just don't add up. Check your spelling!"
    else:
        return "You don't even have any cash!"
