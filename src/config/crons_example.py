import src.lib.triggers as triggers

crons = {
    "crons": {
        "#channel": [
            #time, run, callback
            (600, True, triggers.trigger_less_than_200_for_all) #reloads points to 200 every hour
            #(600, True, treats.cron),  # treat handed out every 10 minutes
        ],
    }
}
