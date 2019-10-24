import re

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
  

    parts = message.split('&')
    command = parts[0]

    parameters = parts[1:] if len(parts) > 2 else parts[1] if len(parts) > 1 else None

    rejoin = '&'.join(parts[1:])

    if (len(parts) > 2 and 'duration' in parts[2]):
        duration = int(re.search(r'=(?P<dur>\d*)', parts[2]).group('dur'))
        print 'found duration in parts[2]! {}'.format(duration)
        # newparts = [parts[:1] , parts[3:] ]
        del parts[2]
        print('new parts: {}'.format(parts))

    reparts = rejoin.split('&')
    rejoin2 = '&'.join(reparts[1:])
    print('rejoin2: {}'.format(rejoin2))
    match = re.search(r'duration=(\d*)&', rejoin2)
    if match:
        duration = int(match.group(1))
        start = match.start(0)
        end = match.end(0)
        # rejoin2 = rejoin2[end:]
        rejoin2 = rejoin2[:start] + rejoin2[end:]
        print 'found duration in rejoin2! {}, start: {}, end: {}, rejoin2: {}'.format(duration, start, end, rejoin2)



    if ('duration' in message):
        print 'found duration in message!'

    print 'command: {}, parts: {}, parts.len: {}, parameters: {}, rejoin: {}'.format(command, parts, len(parts), parameters, rejoin)
    commands.get(command, commands.get('unknown'))(parameters)


# run('next')
# run('previous')
# run('reload')
# run('stop')
# run('play')
# run('current_asset_id')
# run('asset&id_767676')
# run('asset&id_767676&another')
# run('asset&id_767676&another&a_third')
run('asset&id_767676&duration=25&another&a_third&fourth')
#run('asset?id_767676&another&a_third')
