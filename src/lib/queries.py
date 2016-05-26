#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
from datetime import datetime
test_users = ["user", "singlerider", "testuser"]


class Database:

    def __init__(self, name="twitch.db"):
        self.name = name
        self.con = lite.connect(self.name, check_same_thread=False)

    def initiate(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY,
                    username TEXT, points INT,
                    channel TEXT, last_changed_below_200 TEXT);
                """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS custom_commands(
                    id INTEGER PRIMARY KEY, channel TEXT,
                    created_by TEXT, command TEXT,
                    response TEXT, times_used INT
                    , user_level TEXT);
                """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS quotes(
                    id INTEGER PRIMARY KEY, channel TEXT,
                    created_by TEXT, quote TEXT,
                    quote_number INT, game TEXT);
                """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS channel_info(
                    id INTEGER PRIMARY KEY, channel TEXT,
                    stream_id INTEGER DEFAULT 0,
                    twitch_oauth TEXT DEFAULT '',
                    twitchalerts_oauth TEXT DEFAULT '',
                    last_time_points_reset TEXT);
                """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS channel_data(
                    id INTEGER PRIMARY KEY, channel TEXT,
                    username TEXT, data_type TEXT);
                """)

    def add_user(self, users, channel):
        time = datetime.strftime(datetime.utcnow(), "%Y %m %d %H %M %S")
        user_tuples = [(user, channel, time, user, channel, time) for user in users]
        with self.con:
            cur = self.con.cursor()
            cur.executemany("""
                INSERT INTO users(id, username, points, channel, last_changed_below_200)
                    SELECT NULL, ?, 0, ?, ?
                    WHERE NOT EXISTS(
                        SELECT 1 FROM users WHERE username = ?
                        AND channel = ? AND last_changed_below_200 = ?);
                """, user_tuples)

    def remove_user(self, user="testuser", channel="testchannel"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                DELETE FROM users WHERE username = ? and channel = ?;
                """, [user, channel])

    def get_user(self, user="testuser", channel="testchannel"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT * FROM users WHERE username = ? and channel = ?
                """, [user, channel])
            user_data = cur.fetchone()
            return user_data

    def modify_points(self, user="testuser", channel="testchannel", points=5):
        with self.con:
            #Tries to start a trigger everytime points are modified
            last_points = self.get_points(channel, user)[0]
            trigger_more_than_5000(user, channel, last_points, points)
            
            cur = self.con.cursor()
            cur.execute("""
                UPDATE users SET points = points + ? WHERE username = ?
                    AND channel = ?;
                """, [points, user, channel])

    def add_command(
            self, user="testuser", command="!test",
            response="{} check this out", user_level="reg",
            channel="testuser"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                INSERT INTO custom_commands(
                    id, channel, created_by, command, response,
                    times_used, user_level)
                    SELECT NULL, ?, ?, ?, ?, 0, ?
                    WHERE NOT EXISTS(
                        SELECT 1 FROM custom_commands
                            WHERE command = ? and channel = ?);
                """, [channel, user, command, response,
                        user_level, command, channel])

    def remove_command(self, command="!test", channel="testuser"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                DELETE FROM custom_commands
                    WHERE command = ? AND channel = ?;
                """, [command, channel])

    def modify_command(
            self, command="!test", response="different response",
            channel="testuser", user_level="mod"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                UPDATE custom_commands SET response = ?, user_level = ?
                    WHERE command = ? AND channel = ?;
                """, [response, user_level, command, channel])

    def increment_command(self, command="!test", channel="testuser"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                UPDATE custom_commands SET times_used = times_used + 1
                    WHERE command = ? AND channel = ?;
                """, [command, channel])

    def get_command(self, command="!test", channel="testuser"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT * FROM custom_commands
                    WHERE command = ? AND channel = ?;
                """, [command, channel])
            command_data = cur.fetchone()
            return command_data

    def add_quote(
            self, channel="testchannel", user="testuser",
            quote="quote", game="testgame"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT count(0) FROM quotes WHERE channel = ?
                """, [channel])
            count = cur.fetchone()[0]
            cur.execute("""
                INSERT INTO quotes VALUES (NULL, ?, ?, ?, ?, ?)
                """, [channel, user, quote, count + 1, game])

    def remove_quotes(self, channel="testchannel"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                DELETE FROM quotes WHERE channel = ?
                """, [channel])

    def get_quote(self, channel="testchannel"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT * FROM quotes WHERE channel = ?
                    ORDER BY RANDOM() LIMIT 1;
                """, [channel])
            quote = cur.fetchone()
            return quote

    def get_cash_rank(self, user="testuser", channel="testchannel"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT a1.username, a1.points, a1.channel,
                        COUNT (a2.points) points_rank
                    FROM users a1, users a2
                    WHERE a1.points < a2.points
                        OR (a1.points=a2.points
                            AND a1.username = a2.username)
                    GROUP BY a1.username, a1.points
                    HAVING a1.username = ?
                    AND a1.channel = ?
                    ORDER BY a1.points DESC, a1.username DESC;
                """, [user, channel])
            rank_data = cur.fetchone()
            return rank_data

    def get_top10(self, channel="testchannel"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT * FROM users WHERE channel = ?
                    ORDER BY points DESC LIMIT 10;
                """, [channel])
            rank_data = cur.fetchall()
            return rank_data

    def get_channel_id(self, channel="testchannel"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT id, channel FROM channel_info WHERE channel = ?;
                """, [channel])
            channel_id = cur.fetchone()
            return channel_id

    def get_stream_id(self, channel="testchannel"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT channel, stream_id FROM channel_info WHERE channel = ?;
                """, [channel])
            stream_id = cur.fetchone()
            return stream_id

    def update_stream_id(self, channel="testchannel", stream_id=1234567):
        cur = self.con.cursor()
        cur.execute("""
            UPDATE channel_info SET stream_id = ? WHERE channel = ?;
            """, [stream_id, channel])

    def add_channel_id(self, id=12345, channel="testchannel"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                INSERT INTO channel_info(
                    id, channel)
                    SELECT ?, ?
                    WHERE NOT EXISTS(
                        SELECT 1 FROM channel_info
                            WHERE channel = ?);
                """, [id, channel, channel])

    def remove_channel_info(self, id=12345, channel="testchannel"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                DELETE FROM channel_info WHERE id = ? OR channel = ?;
                """, [id, channel])

    def get_channel_data_by_user(self, user="testuser",
            channel="testchannel", data_type="host"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT channel, username, data_type FROM channel_data
                    WHERE username = ? AND channel = ? AND data_type = ?;
                """, [user, channel, data_type])
            channel_data = cur.fetchall()
            return channel_data

    def get_channel_data_by_data_type(self, channel="testchannel",
            data_type="host"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                SELECT id, channel, username, data_type FROM channel_data
                    WHERE channel = ? AND data_type = ?
                """, [channel, data_type])
            channel_data = cur.fetchall()
            return channel_data

    def insert_channel_data(self, user="testuser", channel="testchannel",
            data_type="host"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                INSERT INTO channel_data(
                    id, channel, username, data_type)
                    SELECT NULL, ?, ?, ?
                    WHERE NOT EXISTS(
                        SELECT 1 FROM channel_data
                            WHERE channel = ? AND username = ?
                            AND data_type = ?);
                """, [channel, user, data_type, channel, user, data_type])

    def remove_channel_data(self, channel="testchannel", data_type="host"):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                DELETE FROM channel_data WHERE channel = ? AND data_type = ?;
                """, [channel, data_type])
                
    def get_points(self, channel, username):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
            SELECT points FROM users
            WHERE username = ? AND channel = ?;
            """, [username, channel])
            points = cur.fetchone()
            return points
            
    def set_points(self, channel, username, points):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                UPDATE users SET points = ? WHERE username = ?
                    AND channel = ?;
                """, [points, username, channel])
                
    def get_last_changed_below_200(self, channel, username):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
            SELECT last_changed_below_200 FROM users
            WHERE username = ? AND channel = ?;
            """, [username, channel])
            date = cur.fetchone()
            return date
            
    def set_last_changed_below_200(self, channel, username, date):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                UPDATE users SET last_changed_below_200 = ? WHERE username = ?
                    AND channel = ?;
                """, [date, username, channel])
                
    def get_last_time_points_reset(self, channel):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
            SELECT last_time_points_reset FROM channel_info
            WHERE channel = ?;
            """, [channel])
            date = cur.fetchone()
            return date
            
    def set_last_time_points_reset(self, channel, date):
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                UPDATE channel_info SET last_time_points_reset = ? WHERE channel = ?;
                """, [date, channel])
                
    def get_all_usernames(self, channel):
        with self.con:
            usernames = []
            cur = self.con.cursor()
            cur.execute("""
                SELECT username FROM users WHERE channel = ?
                """, [channel])
            usernames_tuples = cur.fetchall()
            for usernames_tuple in usernames_tuples:
                usernames.append(usernames_tuple[0])
            return usernames

if __name__ == "__main__":
    channel = "testchannel"
    db = Database("test.db")
    db.initiate()
    db.add_user(test_users, channel)
    print db.get_user()
    db.modify_points()
    print db.get_user()
    db.add_command()
    db.increment_command()
    print db.get_command()
    db.increment_command()
    db.modify_command()
    print db.get_command()
    db.increment_command()
    print db.get_command()
    db.add_quote()
    print db.get_quote()
    print db.get_cash_rank()
    print db.get_top10()
    print db.get_channel_id()
    db.add_channel_id()
    db.update_stream_id()
    print db.get_channel_id()
    db.insert_channel_data()
    print db.get_channel_data_by_data_type()
    raw_input("press enter to delete the test entries")
    db.remove_command()
    for user in test_users:
        db.remove_user(user)
    db.remove_quotes()
    db.remove_channel_info()
    db.remove_channel_data()
    
    
    
from src.lib.triggers import *