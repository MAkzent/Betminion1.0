import globals
import time
import sys
from threading import Thread

def initialize(chan, delay):
    BetsThread(globals.irc, chan, delay).start()
    
class BetsThread(Thread):

    def __init__(self, irc, chan, delay):
        Thread.__init__(self, target=self.main)
        self.daemon = True
        self.delay = delay
        self.now = time.time()
        self.chan = chan
        self.irc = irc

    def main(self):
        begin_resp = "Bets will close in {0} seconds!".format(self.delay)
        end_resp = "Bets are now closed!"
        time_left = "{0} seconds of betting remains!".format(self.delay / 2)
        self.irc.send_message(self.chan, begin_resp)
        time.sleep(float(self.delay / 2))
        self.irc.send_message(self.chan, time_left)
        time.sleep(float(self.delay / 2))
        self.irc.send_message(self.chan, end_resp)
        globals.BETS = False
        
        sys.exit()