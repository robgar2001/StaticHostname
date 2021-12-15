from functools import partial
import logger


class Message:
    def __init__(self, line, irc):
        self.irc = irc
        self.line = str.split(str.rstrip(line))
        line = self.line
        self.type = 'startup'

        if len(line) < 2:
            logger.log('Message to small to parse')
            return

        place1_args = {'PING': partial(self.ping_response, line)}
        place1f = place1_args.get(line[0], False)
        if place1f:
            place1f()
            return

        def privmsg():
            self.type = 'privmsg'
            message = ''.join([line[i] + ' ' for i in range(3, len(line))]).lstrip(':').strip(':')
            self.text = self.irc.cipher.decrypt(message)

        place2_args = {'MODE': partial(self.irc.__setattr__, 'start_up_finished', True),
                       'PRIVMSG': privmsg}

        place2f = place2_args.get(line[1], False)
        if place2f:
            place2f()

    def __str__(self):
        return self.text

    def ping_response(self, line):
        logger.log('Pong!')
        self.irc.socket.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))
