import socket
import threading
from encryption import encrypt, decrypt
from requests import get
import time


class Server:
    def __init__(self, host="irc.irchighway.net", port=6669, nick='shs123'):
        self.HOST = host
        self.PORT = port

        self.NICK = nick
        self.sender = "shc123"

        self.poller = IPPoller()

        self.readbuffer = ""
        self.receive_buffer_size = 1024

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
            readbuffer = readbuffer + self.s.recv(self.receive_buffer_size).decode("UTF-8")
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
                    self.sender = ""
                    for char in line[0]:
                        if (char == "!"):
                            break
                        if (char != ":"):
                            self.sender += char
                    size = len(line)
                    i = 3
                    message = ""
                    while (i < size):
                        message += line[i] + " "
                        i = i + 1
                    message.lstrip(":")
                    message = message.strip(":")

                    request = decrypt(message)[:-1]
                    print(request)
                    if request == 'ip':
                        self.send_message(message=self.poller.latest_ip_update, to=self.sender)

            ip = self.poller.ip
            if ip != self.poller.latest_ip_update:
                self.send_message(message=ip, to=self.sender)
                self.poller.latest_ip_update = ip

    def send_message(self, message, to):
        self.s.send(bytes("PRIVMSG %s %s \r\n" % (to, encrypt(str(message))), "UTF-8"))


class IPPoller:
    def __init__(self):
        self.latest_ip_update = None
        self.ip = None
        self.thread = threading.Thread(target=self.poll)
        self.thread.start()

    def poll(self):
        while 1:
            self.ip = self.get_ip
            time.sleep(60*5)

    @property
    def get_ip(self):
        return get('https://api.ipify.org').text


s = Server()
t = threading.Thread(target=s.start)
t.start()


