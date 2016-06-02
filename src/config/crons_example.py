import src.lib.triggers as triggers

crons = {
    "crons": {
        "#channel": [
            #time, run, callback
            (3600, True, triggers.trigger_less_than_200_for_all), #reloads points to 200 every hour
            (4800, True, triggers.trigger_clear_bets) #clears bets and dumps to csv file. Run only on one channel!
            #(600, True, treats.cron),  # treat handed out every 10 minutes
        ],
    }
}
