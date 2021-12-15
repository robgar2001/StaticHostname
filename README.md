# StaticHostname
Static hostname provider

Ever needed a hostname for a public ipv4 address but don't feel like using dynamicDNS?
Well, this project is aimed at solving that exact issue!

The plan is to send an IP update encrypted over public IRC channels.
At the receiver end you can host a dns server, where a chosen hostname will resolve the dynamic ipv4 address.
Using this method, it will allow access from the receiver network to the target network by a static hostname.
