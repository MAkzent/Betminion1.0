from src.lib.queries import Database
from datetime import datetime
import globals

#Main Bets class that contains all of the bidders data and distributes profit
#Constructed in start.py
class Bets:

    def __init__(self):
        self.irc = globals.irc
        self.channel = globals.CURRENT_CHANNEL
        self.chan = "#" + self.channel
        self.db = Database()
        #self.bets_started = datetime.strptime(self.db.get_bets_started(self.channel)[0], "%Y %m %d %H %M %S")
        #Generates list of tuples(username, amount, outcome, date) that only consists of bidders that bet after the bets have started
        self.bets_data = [x for x in self.db.get_bets_data(self.channel) if datetime.strptime(x[3], "%Y %m %d %H %M %S") > datetime.strptime(self.db.get_bets_started(self.channel)[0], "%Y %m %d %H %M %S")]
        
    def calculate_total_points(self):
        total_points = 0
        for bidder in self.bets_data:
            total_points += bidder[1]
            
        return total_points
        
    def calculate_winning_points(self, outcome):
        winning_points = 0
        for bidder in self.bets_data:
            if bidder[2] == outcome:
                winning_points += bidder[1]
            
        return winning_points
    
    #Called from outcome.py
    def distribute_profit(self, outcome):
        bets_total = self.calculate_total_points()
        bets_winning = self.calculate_winning_points(outcome)
        
        try:
            profit = float(bets_total)/bets_winning
        except ZeroDivisionError:
            msg = "Sorry, there are no winners"
            self.irc.send_message(self.chan, msg)
            return
        
        try:
            for bidder in self.bets_data:
                if bidder[2] == outcome:
                    winnings = int(profit*bidder[1])
                    self.db.modify_points(bidder[0], winnings)
                    msg = "/w {0} Congrats! You won {1} points!".format(bidder[0], winnings)
                    self.irc.send_message(self.chan, msg)
                else:
                    msg = "/w {0} Feelsbadman, maybe you will win next time".format(bidder[0])
                    self.irc.send_message(self.chan, msg)
                
        except Exception as error:
            print error
            msg = "Sorry, there was an error distributing profit"
            self.irc.send_message(self.chan, msg)
            return
        
        msg = "Winnings have been released!"
        self.irc.send_message(self.chan, msg)