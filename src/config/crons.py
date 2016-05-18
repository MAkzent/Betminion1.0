import src.lib.commands.hosts as hosts

crons = {
    "crons": {
        "#ravenhart007": [
            #time, run, callback
            (300, True, hosts.cron),  # pokemon released every 20 minutes
            #(600, True, treats.cron),  # treat handed out every 10 minutes
        ],
    }
}
