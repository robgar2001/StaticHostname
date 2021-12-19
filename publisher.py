from transport.irc.irc import IRCClient
from requests import get


class Publisher(IRCClient):
    subscriber = 'subscriberb1232'

    @property
    def get_ip(self):
        return get('https://api.ipify.org').text

    def parser(self, message):
        if str(message) == 'ip?':
            self.send_message(message=self.get_ip, to=self.subscriber)


publisher = Publisher(name='publisherb1232')
