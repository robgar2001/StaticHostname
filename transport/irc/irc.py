import socket
import threading
import logger
from transport.encryption.AES import Cipher
from transport.irc import irc_message


class IRCClient:
    encoding = 'utf-8'

    def __init__(self, host='irc.irchighway.net', port=6669, name='shc123'):
        logger.log('Creating irc instance to : %s %i' % (host, port))
        logger.log('Name will be %s' % name)
        self.host = host
        self.port = port

        self.cipher = Cipher(key='1232')

        self.name = name
        self.start_up_finished = False
        self.readbuffer = ''  # used to cache text, cause socket is a stream

        self.socket = socket.socket()

        self.thread = threading.Thread(target=self.connect_to_irc)
        self.thread.start()

    def connect_to_irc(self):
        logger.log('Connecting to server...')
        while True:
            try:
                self.socket.connect((self.host, self.port))
                break
            except TimeoutError as e:
                logger.log('Failed to connect')

        self.socket.send(bytes("NICK %s\r\n" % self.name, self.encoding))
        self.socket.send(bytes("USER %s %s bla :%s\r\n" % (self.name, self.host, self.name), self.encoding))
        self.socket.send(bytes("/JOIN #irchighway\r\n", self.encoding))
        self.start()

    def start(self):
        while True:
            readbuffer = self.readbuffer
            readbuffer = readbuffer + self.socket.recv(1024).decode(self.encoding)
            temp = str.split(readbuffer, "\n")
            readbuffer = temp.pop()

            for line in temp:
                if len(line) >= 2:
                    message = irc_message.Message(line=line, irc=self)
                    self.parser(message=message) if message.type != 'startup' else None

    def parser(self, message):
        logger.log(message)

    def send_message(self, message, to):
        logger.log('Sending command: %s to %s ' % (message, to))
        self.socket.send(bytes("PRIVMSG %s %s\r\n" % (to, self.cipher.encrypt(message)), "UTF-8"))


irc = IRCClient()
