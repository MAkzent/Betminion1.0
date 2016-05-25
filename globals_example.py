CURRENT_CHANNEL = ""
CURRENT_USER = ""
VARIABLE = ""
channel_info = {}
#Tells if there are bets going on right now
BETS = False
#Contains all data on betters. It will be constructed as an instance of Bets class once "!start" is called
BETS_DATA = ""
#For !result
LAST_RESULT = ""
irc = None
