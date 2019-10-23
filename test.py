def skip_asset(back=False):
    print('=>skip_asset({})'.format(back))

def navigate_to_asset(asset_id):
    #isinstance(asset_id, list)
    print('=>navigate_to_asset({})'.format(asset_id))

def stop_loop():
    print('=>stop_loop()')

def play_loop():
    print('=>play_loop()')

def command_not_found():
    print('=>command_not_found()')

def send_current_asset_id_to_server():
    print('=>send_current_asset_id_to_server()')

def load_settings():
    print('=>load_settings()')

commands = {
    'next': lambda _: skip_asset(),
    'previous': lambda _: skip_asset(back=True),
    'asset': lambda id: navigate_to_asset(id),
    'reload': lambda _: load_settings(),
    'stop': lambda _: stop_loop(),
    'play': lambda _: play_loop(),
    'unknown': lambda _: command_not_found(),
    'current_asset_id': lambda _: send_current_asset_id_to_server()
}


def run(message):

#    print('parms:{}'.format(message.split('&', 2)))

    # if (message.find('?') != -1):
    #     parts = message.split('?')
    #     parameters = parts[1].split('&', 1) if len(parts) > 1 else None
    # else:
    #     parts = message.split('&')
    #     parameters = parts[1] if len(parts) > 1 else None
  

    parts = message.split('&', 2)
    command = parts[0]

    parameters = parts[1:] if len(parts) > 2 else parts[1] if len(parts) > 1 else None

    print 'command: {}, parts: {}, parts.len: {}, parameters: {}'.format(command, parts, len(parts), parameters)
    commands.get(command, commands.get('unknown'))(parameters)


# run('next')
# run('previous')
# run('reload')
# run('stop')
# run('play')
# run('current_asset_id')
run('asset&id_767676')
run('asset&id_767676&another')
run('asset&id_767676&another&a_third')
run('asset&id_767676&another&a_third&fourth')
#run('asset?id_767676&another&a_third')
