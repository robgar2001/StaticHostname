from transport.irc.irc import IRCClient
import logger

c = IRCClient(name='subscriberb1232')
logger.log('Subscriber is starting, now starting request thread')
while True:
    if c.start_up_finished:
        receiver = 'publisherb1232'
        command = input('Command: \n')
        c.send_message(to=receiver, message=command)
