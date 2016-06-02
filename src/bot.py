"""
Custom Twitch Chat Moderator Bot for Twitch.tv

By Shane Engelman me@5h4n3.com @shaneengelman

Made for twitch.tv/ravenhart007
"""

import sys

import globals
import lib.functions_commands as commands
import lib.irc as irc_
import src.config.crons as crons
import src.lib.command_headers
import src.lib.cron as cron
import src.lib.twitch as twitch
from lib.functions_general import *
from src.lib.queries import Database
from src.lib.twitch import get_dict_for_users

reload(sys)
sys.setdefaultencoding("utf8")


END = False

class Roboraj(object):

    def __init__(self, config):
        self.db = Database()
        self.db.initiate()
        self.config = config
        self.crons = crons
        src.lib.command_headers.initalizeCommands(config)
        self.irc = irc_.irc(config)
        # start threads for channels that have cron messages to run
        cron.initialize_crons(self.irc, self.crons.crons.get("crons", {}))
        cron.initialize_channel_id_check(self.config)
        globals.irc = self.irc

    def run(self):

        # This is a very handy function, so I'm not deleting it yet
        
        
        # def check_for_sub(channel, username, message):
            # # >> :twitchnotify!twitchnotify@twitchnotify.tmi.twitch.tv PRIVMSG #curvyllama :KiefyWonder subscribed for 5 months in a row!
            # # >> :twitchnotify!twitchnotify@twitchnotify.tmi.twitch.tv PRIVMSG #curvyllama :KiefyWonder just subscribed!
            # # Photo_phocus just subscribed to jonsandman!
            # # HermanNugent subscribed to JonSandman for 7 months in a row!
            # # first sub points = 1000
            # # resub = 250
            # db = Database()
            # try:
                # channel = channel.lstrip("#")
                # message_split = message.rstrip("!").split()
                # subbed_user = message_split[0].lower()
                # if message_split[1] == "just" and len(message_split) < 4:
                    # points = 1000
                    # db.add_user([subbed_user], channel)
                    # db.modify_points(subbed_user, channel, points)
                    # resp = "/me {0} just subscribed for the first time!\
 # {1} cash for you!".format(subbed_user, points)
                    # self.irc.send_message("#" + channel, resp)
                # elif message_split[1] == "subscribed" and len(message_split) < 9:
                    # months_subbed = message_split[3]
                    # points = 250
                    # db.add_user([subbed_user], channel)
                    # db.modify_points(subbed_user, channel, points)
                    # resp = "/me {0} has just resubscribed for {1} months \
# straight and is getting {2} cash!".format(subbed_user, months_subbed, points)
                    # self.irc.send_message("#" + channel, resp)
            # except Exception as error:
                # print error
                      
                
        # For admin created commands. Not that useful but I'll keep it in case I have to implement it
        
        
        # def custom_command(channel, message, username, elements):
            # db = Database()
            # command = elements[3]
            # chan = channel.lstrip("#")
            # replacement_user = username
            # if len(message) > 1:
                # replacement_user = message[1]
            # if elements[6] == "mod":
                # user_dict, __ = get_dict_for_users()
                # if username in user_dict["chatters"]["moderators"]:
                    # resp = elements[4].replace("{}", replacement_user).replace(
                        # "[]", str(elements[5]))
                    # self.irc.send_message(channel, resp)
                    # db.increment_command(command, chan)
                # else:
                    # resp = "This is a moderator-only command"
                    # self.irc.send_message(channel, resp)
            # elif elements[6] == "reg":
                # resp = elements[4].replace("{}", replacement_user).replace(
                    # "[]", str(elements[5]))
                # self.irc.send_message(channel, resp)
                # db.increment_command(command, chan)
                
        #Main process
        while True:
            try:
                data = self.irc.nextMessage()
                if self.irc.check_for_message(data):
                    message_dict = self.irc.get_message(data)
                    channel = message_dict['channel']
                    message = message_dict['message']
                    username = message_dict['username']
                elif self.irc.check_for_whisper(data):
                    message_dict = self.irc.get_whisper(data)
                    channel = self.config["channels"][0]
                    message = message_dict['message']
                    username = message_dict['username']
                    if message.startswith("!"):
                        resp = '/w %s Please type your command in the channel chat' % (username)
                        pbot(resp, channel)
                        self.irc.send_message(channel, resp)
                    continue
                else:
                    continue
                globals.CURRENT_CHANNEL = channel.lstrip('#')
                globals.CURRENT_USER = username
                chan = channel.lstrip("#")
                #Part of the "subscribed" functionality
                # if username == "twitchnotify":
                    # check_for_sub(channel, username, message)
                part = message.split(' ')[0]
                valid = False
                if commands.is_valid_command(message):
                    valid = True
                if commands.is_valid_command(part):
                    valid = True
                if not valid:
                    continue
                self.handleCommand(part, channel, username, message)
            except Exception as error:
                print error

    def handleCommand(self, command, channel, username, message):
        # parse arguments
        # if command is space case then
        #   !foo bar baz
        # turns into
        #   command = "!foo", args=["bar baz"]
        # otherwise it turns into
        #   command = "!foo", args=["bar", "baz"]
        # print("Inputs:", command, channel, username, message)
        if command == message:
            args = []
        else:
            # default to args = ["bar baz"]
            args = [message[len(command) + 1:]]
        if not commands.check_is_space_case(command) and args:
            # if it's not space case, break the arg apart
            args = args[0].split(" ")
        if commands.is_on_cooldown(command, channel):
            pbot('Command is on cooldown. (%s) (%s) (%ss remaining)' % (
                command, username, commands.get_cooldown_remaining(
                    command, channel)), channel)
            return
        if commands.check_has_user_cooldown(command):
            if commands.is_on_user_cooldown(command, channel, username):
                resp = "/w " + username + " Sorry! You've got " + str(
                    commands.get_user_cooldown_remaining(
                        command, channel, username)) + \
                    " seconds before you can do that again!"
                self.irc.send_message(channel, resp)
                return
            commands.update_user_last_used(command, channel, username)
        pbot('Command is valid and not on cooldown. (%s) (%s)' %
             (command, username), channel)
        # Check for and handle the simple non-command case.
        cmd_return = commands.get_return(command)
        if cmd_return != "command":
            # it's a return = "some message here" kind of function
            resp = '/w %s %s' % (username, cmd_return)
            commands.update_last_used(command, channel)
            self.irc.send_message(channel, resp)
            return
        # if there's a required userlevel, validate it.
        if commands.check_has_ul(username, command):
            if username.lower() != self.config["username"].lower():
                resp = '/w %s %s' % (
                    username, "This is a moderator-only command!")
                pbot(resp, channel)
                self.irc.send_message(channel, resp)
                return
        result = commands.pass_to_function(command, args)
        commands.update_last_used(command, channel)
        if result:
            resp = '/w %s %s' % (username, result)
            pbot(resp, channel)
            self.irc.send_message(channel, resp)
