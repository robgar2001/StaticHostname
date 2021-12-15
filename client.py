import socket
import threading
from encryption import Cipher


class Client:
    def __init__(self, host='irc.irchighway.net', port=6669, nick='shcc123'):
        self.HOST = host
        self.PORT = port

        self.NICK = nick
        self.sender = ""
        self.init_communication_finished = False
        self.start_up_finished = False
        self.latest_ip = None

        self.cipher = Cipher(key='1232')

        self.readbuffer = ""

        self.s = socket.socket()

    def start(self):
        while True:
            try:
                self.s.connect((self.HOST, self.PORT))
                break
            except:
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
                print(line)
                line = str.rstrip(line)
                line = str.split(line)
                if len(line) < 2:
                    continue
                if (line[0] == "PING"):
                    self.s.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))
                if (line[1] == "PRIVMSG"):
                    for char in line[0]:
                        if (char == "!"):
                            break
                    size = len(line)
                    i = 3
                    message = ""
                    while (i < size):
                        message += line[i] + " "
                        i = i + 1
                    message.lstrip(":")
                    message = message.strip(":")
                    decrypted_message = self.cipher.decrypt(message)[:-1]
                    self.latest_ip = decrypted_message
                    print(decrypted_message)

                if (line[1] == 'MODE'):
                    self.start_up_finished = True

    def send_message(self, message, to):
        print('Sending command: ', message, 'to', to)
        secret = self.cipher.encrypt(message)
        print('Cipher text: %s' % secret)
        self.s.send(bytes("PRIVMSG %s %s\r\n" % (to, secret), "UTF-8"))


c = Client()
t = threading.Thread(target=c.start)
t.start()

while True:
    if c.start_up_finished:
        receiver = 'shc123'
        command = input('Command: \n')
        if not c.latest_ip:
            c.send_message(to=receiver, message=command)
        else:
            print(c.latest_ip)
