import globals

commands = {

    '!commands': {
        'limit': 0,
        'return': 'command',
        'argc': 0,
        'usage': '!commands'
    },

    '!followers': {
        'limit': 30,
        'return': 'command',
        'argc': 0,
        'usage': '!followers'
    },

    '!follower': {
        'limit': 0,
        'return': 'command',
        'argc': 1,
        'usage': '!follower [username]'
    },

    '!uptime': {
        'limit': 15,
        'return': 'command',
        'argc': 0,
        'usage': '!uptime',
        'user_limit': 5
    },

    '!stream': {
        'limit': 60,
        'return': 'command',
        'argc': 0,
        'usage': '!stream'
    },

    '!popularity': {
        'limit': 0,
        'argc': 1,
        'return': 'command',
        'space_case': True,
        'usage': '!popularity [name_of_game]'
    },

    '!follow': {
        'limit': 0,
        'argc': 1,
        'return': 'command',
        'usage': '!follow [streamer_username]',
        'ul': 'mod'
    },

    '!donation': {
        'limit': 0,
        'argc': 2,
        'return': 'command',
        'usage': '!donation [username] [dollar_amount]',
        'ul': 'mod'
    },

    '!cash': {
        'limit': 0,
        'argc': 3,
        'return': 'command',
        'usage': '!cash ["add"/"remove"/"set"] [username]',
        'space_case': True,
        'optional': True
    },

    '!add': {
        'limit': 0,
        'argc': 3,
        'return': 'command',
        'usage': '!add [command] [user_level("mod"/"reg") [response (\"{}\" replaces with username, \"[]\" replaces with counter)]'
    },

    '!edit': {
        'limit': 0,
        'argc': 3,
        'return': 'command',
        'usage': '!edit [command] [user_level("mod"/"reg") [response (\"{}\" replaces with username, \"[]\" replaces with counter)]'
    },

    '!rem': {
        'limit': 0,
        'argc': 1,
        'return': 'command',
        'usage': '!rem [command]'
    },

    '!test': {
        'limit': 0,
        'user_limit': 15,
        'return': "NOT ON COOLDOWN, apparently",
        'usage': '!test'
    },

    '!addquote': {
        'limit': 0,
        'argc': 1,
        'user_limit': 15,
        'return': 'command',
        'usage': '!addquote [quote]',
        'space_case': True
    },

    '!quote': {
        'limit': 0,
        'argc': 0,
        'user_limit': 5,
        'return': 'command',
        'usage': '!quote'
    },

    '!gamble': {
        'limit': 0,
        'argc': 1,
        'return': 'command',
        'usage': '!gamble [points_to_gamble_with]'
    },

    '!chance': {
        'limit': 0,
        'argc': 0,
        'return': 'command',
        'usage': '!chance',
        'user_limit': 1800
    },

    '!join': {
        'limit': 0,
        'argc': 0,
        'return': 'command',
        'usage': '!join'
    },

    '!pot': {
        'limit': 0,
        'argc': 0,
        'return': 'command',
        'usage': '!pot'
    },

    '!gift': {
        'limit': 0,
        'argc': 2,
        'return': 'command',
        'usage': '!gift [username] [amount]'
    },

    '!top10': {
        'limit': 0,
        'return': 'command',
        'user_limit': 60,
        'usage': "!top10",
        'argc': 0
    },

    '!hosts': {
        'limit': 0,
        'return': 'command',
        'usage': '!hosts',
        'argc': 0
    }
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
