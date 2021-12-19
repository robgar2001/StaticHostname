import threading
import socketserver
from dnslib import *
import logger


class DomainName(str):
    def __getattr__(self, item):
        return DomainName(item + '.' + self)


subscriber = None


def dns_response(data):
    if subscriber.start_up_finished:
        subscriber.send_message('ip?')
    while 1:
        IP = subscriber.ip
        if subscriber.ip_updated == True:
            break
    subscriber.ip_updated = False

    D = DomainName('mynconet.be.')
    TTL = 60 * 5
    soa_record = SOA(
        mname=D.ns1,  # primary name server
        rname=D.andrei,  # email of the domain administrator
        times=(
            201307231,  # serial number
            60 * 60 * 1,  # refresh
            60 * 60 * 3,  # retry
            60 * 60 * 24,  # expire
            60 * 60 * 1,  # minimum
        )
    )
    ns_records = [NS(D.ns1), NS(D.ns2)]
    records = {
        D: [A(IP), AAAA((0,) * 16), MX(D.mail), soa_record] + ns_records,
        D.ns1: [A(IP)],  # MX and NS records must never point to a CNAME alias (RFC 2181 section 10.3)
        D.ns2: [A(IP)],
        D.mail: [A(IP)],
        D.andrei: [CNAME(D)],
    }

    request = DNSRecord.parse(data)
    reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)

    qname = request.q.qname
    qn = str(qname)
    qtype = request.q.qtype
    qt = QTYPE[qtype]

    if qn == D or qn.endswith('.' + D):
        for name, rrs in records.items():
            if name == qn:
                for rdata in rrs:
                    rqt = rdata.__class__.__name__
                    if qt in ['*', rqt]:
                        reply.add_answer(RR(rname=qname, rtype=getattr(QTYPE, rqt), rclass=1, ttl=TTL, rdata=rdata))

        for rdata in ns_records:
            reply.add_ar(RR(rname=D, rtype=QTYPE.NS, rclass=1, ttl=TTL, rdata=rdata))

        reply.add_auth(RR(rname=D, rtype=QTYPE.SOA, rclass=1, ttl=TTL, rdata=soa_record))

    print("---- Reply:\n", reply)

    return reply.pack()


class UDPRequestHandler(socketserver.BaseRequestHandler):
    def get_data(self):
        return self.request[0].strip()

    def send_data(self, data):
        return self.request[1].sendto(data, self.client_address)

    def handle(self):
        logger.log('Request pair (%s, %s)' % (self.client_address[0], self.client_address[1]))
        try:
            data = self.get_data()
            self.send_data(dns_response(data))
        except Exception as e:
            print(str(e))


class DNSServer:
    host = 'localhost'
    port = 53

    def __init__(self, ip_subscriber):
        logger.log("Starting nameserver...")
        udp_server = socketserver.ThreadingUDPServer((self.host, self.port), UDPRequestHandler)

        thread = threading.Thread(target=udp_server.serve_forever)
        thread.start()
        logger.log('DNSServer thread started')

        try:
            while 1:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            udp_server.shutdown()
