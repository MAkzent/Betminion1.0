from src.lib.queries import Database
import globals

class Bets:

    def __init__(self):
        self.bets_data = []
        self.irc = globals.irc
        self.channel = globals.CURRENT_CHANNEL
        self.chan = "#" + self.channel

    def add_bidder(self, username, amount, bet):
        self.bets_data.append({"username": username, "amount": amount, "bet": bet})
        
    def calculate_total_points(self):
        total_points = 0
        for bidder in self.bets_data:
            total_points += bidder["amount"]
            
        return total_points
        
    def calculate_winning_points(self, outcome):
        winning_points = 0
        for bidder in self.bets_data:
            if bidder["bet"] == outcome:
                winning_points += bidder["amount"]
            
        return winning_points
        
    def distribute_profit(self, outcome):
        db = Database()
        bets_total = self.calculate_total_points()
        bets_winning = self.calculate_winning_points(outcome)
        
        try:
            profit = bets_total/bets_winning
        except ZeroDivisionError:
            msg = "Sorry, there are no winners"
            self.irc.send_message(self.chan, msg)
            return
        
        try:
            for bidder in self.bets_data:
                if bidder["bet"] == outcome:
                    winnings = int(profit*bidder["amount"])
                    db.modify_points(bidder["username"], self.channel, winnings)
                    msg = "/w {0} Congrats! You won {1} points!".format(bidder["username"], winnings)
                    self.irc.send_message(self.chan, msg)
                else:
                    msg = "/w {0} Feelsbadman, maybe you will win next time".format(bidder["username"])
                    self.irc.send_message(self.chan, msg)
                
        except Exception as error:
            print error
            msg = "Sorry, there was an error distributing profit"
            self.irc.send_message(self.chan, msg)
            return
        
        msg = "Winnings have been released!"
        self.irc.send_message(self.chan, msg)
        self.bets_data = []