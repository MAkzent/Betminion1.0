#!/usr/bin/env python2.7
import globals
from src.lib.queries import Database
from src.lib.gamble import Gamble

class Test:

    def __init__(self):
        self.channel = "testchannel"

    def gamble(self):
        globals.channel_info = {self.channel: {"gamble": {
            "time": None, "users": {}}}}
        n = 1
        while n < 11:
            print "---------- test #", n, "----------"
            g = Gamble(channel=self.channel, user="testuser", points=500)
            if not g.check_gamble():
                print "pass | ", g.check_gamble()
            else:
                print "fail | ", g.check_gamble()
            g.initiate_gamble()
            if g.check_gamble():
                print "pass | ", g.check_gamble()
            else:
                print "fail | ", g.check_gamble()
            g.terminate_gamble()
            if not g.check_gamble():
                print "pass | ", g.check_gamble()
            else:
                print "fail | ", g.check_gamble()
            if g.rob_yield():
                print "pass | ", g.rob_yield()
            else:
                print "fail | ", g.rob_yield()
            n += 1

if __name__ == "__main__":
    t = Test()
    t.gamble()
