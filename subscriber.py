from transport.irc.irc import IRCClient
from transport.dns.dnsserver import DNSServer
import transport.dns.dnsserver
import logger


class Subscriber(IRCClient):
    publisher = 'publisherb1232'

    def __init__(self, *args, **kwargs):
        logger.log('Subscriber is starting...')
        self.ip_updated = False
        self.ip = None
        super(Subscriber, self).__init__(*args, **kwargs)

    def send_message(self, message):
        super(Subscriber, self).send_message(message, self.publisher)

    def parser(self, message):
        self.ip = str(message)
        self.ip_updated = True


sub = Subscriber(name='subscriberb1232')
transport.dns.dnsserver.subscriber = sub
dnss = DNSServer(ip_subscriber=sub)


