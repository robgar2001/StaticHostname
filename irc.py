import socket
import threading
from functools import partial

from encryption import Cipher


class IRCClient:
    def __init__(self, host='irc.irchighway.net', port=6669, nick='shc123'):
        self.HOST = host
        self.PORT = port

        self.cipher = Cipher(key='1232')

        self.NICK = nick
        self.sender = ""
        self.init_communication_finished = False
        self.start_up_finished = False

        self.readbuffer = ""

        self.s = socket.socket()

        self.thread = threading.Thread(target=self.start)
        self.thread.start()

    def start(self):
        while True:
            try:
                self.s.connect((self.HOST, self.PORT))
                break
            except TimeoutError as e:
                print('Failed to connect')

        self.s.send(bytes("NICK %s\r\n" % self.NICK, "UTF-8"))
        self.s.send(bytes("USER %s %s bla :%s\r\n" % (self.NICK, self.HOST, self.NICK), "UTF-8"))
        self.s.send(bytes("/JOIN #irchighway\r\n", "UTF-8"))
        reply = self.send_message
        while 1:
            readbuffer = self.readbuffer
            readbuffer = readbuffer + self.s.recv(1024).decode("UTF-8")
            temp = str.split(readbuffer, "\n")
            readbuffer = temp.pop()

            for line in temp:
                if len(line) >= 2:
                    message = Message(line=line, irc=self)
                    self.parser(message=Message)

    def parser(self, message):
        print(message)

    def send_message(self, message, to):
        print('Sending command: ', message, 'to', to)
        self.s.send(bytes("PRIVMSG %s %s\r\n" % (to, self.cipher.encrypt(message)), "UTF-8"))


class Message:
    def __init__(self, line, irc: IRCClient):
        self.irc = irc
        line = str.split(str.rstrip(line))

        place1_args = {'PING': partial(self.ping_response, line)}
        place1f = place1_args.get(line[0], False)
        if place1f:
            place1f()
            return

        if line[1] == "PRIVMSG":
            print('Private message line: ', line)
            for char in line[0]:
                if char == "!":
                    break
            size = len(line)
            i = 3
            message = ""
            while i < size:
                message += line[i] + " "
                i = i + 1
            message.lstrip(":")
            message = message.strip(":")
            decrypted_message = self.irc.cipher.decrypt(message)
            print(decrypted_message)

        if line[1] == 'MODE':
            self.start_up_finished = True

    def ping_response(self, line):
        print('Ping request received', line)
        self.irc.s.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))


irc = IRCClient()
