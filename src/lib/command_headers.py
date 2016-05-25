import globals

#Look up Readme.md
commands = {

    '!commands': {
        'limit': 0,
        'return': 'command',
        'argc': 0,
        'usage': '!commands'
    },

    '!uptime': {
        'limit': 15,
        'return': 'command',
        'argc': 0,
        'usage': '!uptime',
        'user_limit': 5
    },

    '!cash': {
        'limit': 0,
        'argc': 3,
        'return': 'command',
        'usage': '!cash ["add"/"remove"/"set"] [username]',
        'space_case': True,
        'optional': True
    },

    '!test': {
        'limit': 0,
        'user_limit': 15,
        'return': "NOT ON COOLDOWN, apparently",
        'usage': '!test'
    },

    '!pot': {
        'limit': 0,
        'argc': 0,
        'return': 'command',
        'usage': '!pot'
    },

    '!top10': {
        'limit': 0,
        'return': 'command',
        'user_limit': 60,
        'usage': "!top10",
        'argc': 0
    },

    '!points': {
        'limit': 0,
        'return': 'command',
        'user_limit': 5,
        'usage': '!points',
        'argc': 0
    },
    
    '!help': {
        'limit': 0,
        'return': "Lorem Ipsum",
        'user_limit': 5,
        'usage': '!help'
    },
    
    '!start': {
        'limit': 0,
        'return': 'command',
        'user_limit': 5,
        'usage': '!start',
        'ul': 'mod',
        'argc': 0
    },
    
    '!stop': {
        'limit': 0,
        'return': 'command',
        'user_limit': 5,
        'usage': '!stop',
        'ul': 'mod',
        'argc': 0
    },
    
    '!outcome': {
        'limit': 0,
        'return': 'command',
        'user_limit': 5,
        'usage': '!outcome [win/lose]',
        'ul': 'mod',
        'argc': 1
    },
    
    '!win': {
        'limit': 0,
        'return': 'command',
        'user_limit': 5,
        'usage': '!win [amount] or !win [amount_in_percents]%',
        'argc': 1
    },
    
    '!lose': {
        'limit': 0,
        'return': 'command',
        'user_limit': 5,
        'usage': '!lose [amount] or !lose [amount_in_percents]%',
        'argc': 1
    },
    
    '!result': {
        'limit': 0,
        'return': 'command',
        'user_limit': 5,
        'usage': '!result',
        'argc': 0
    },
    
    '!claim': {
        'limit': 0,
        'return': 'command',
        'user_limit': 5,
        'usage': '!claim',
        'argc': 0
    },
}

user_cooldowns = {"channels": {}}


def initalizeCommands(config):
    for channel in config['channels']:
        globals.channel_info[channel.lstrip("#")] = {
            "gamble": {"time": None, "users": {}}}
        user_cooldowns["channels"][channel] = {"commands": {}}
        for command in commands:
            commands[command][channel] = {}
            commands[command][channel]['last_used'] = 0
            if "user_limit" in commands[command]:
                user_cooldowns["channels"][channel]["commands"][command] = {
                    "users": {}}
