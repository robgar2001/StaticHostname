import threading
from transport.irc.irc import IRCClient
from requests import get
import time


class IPPoller:
    def __init__(self):
        self.latest_ip_update = None
        self.ip = None
        self.thread = threading.Thread(target=self.poll)
        self.thread.start()

    def poll(self):
        while 1:
            self.ip = self.get_ip
            time.sleep(60 * 5)

    @property
    def get_ip(self):
        return get('https://api.ipify.org').text


class Publisher(IRCClient):
    subscriber = 'subscriberb1232'

    def __init__(self, *args, **kwargs):
        self.poller = IPPoller()
        super(Publisher, self).__init__(*args, **kwargs)

    def parser(self, message):
        ip = self.poller.ip
        if ip != self.poller.latest_ip_update:
            self.send_message(message=ip, to=self.subscriber)
            self.poller.latest_ip_update = ip
        elif str(message) == 'ip?':
            self.send_message(message=ip, to=self.subscriber)


publisher = Publisher(name='publisherb1232')
