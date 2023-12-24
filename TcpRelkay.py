# import socket
import MsgShare
import scapy.all as scapy
import loguru
import xTrace
'''
TCP forwarding
'''


class TCPForwarding:
    def __init__(self, channel: MsgShare.Channel):
        self.channel = channel

    def forwarding(self):
        """
        forwarding the packet
        """
        try:
            while True:
                # get the packet from the channel
                if self.channel.empty():
                    continue
                pkg = self.channel.pop()
                # get the five tuple of the packet
                sip, dip, sport, dport, flags = xTrace.Sniffer.get_five_tuple(pkg)
                mac = xTrace.Sniffer.get_mac(pkg)
                # use scapy to send the packet
                send_pkg = scapy.Ether(src=mac) / scapy.IP(src=sip, dst=dip) / scapy.TCP(sport=sport, dport=dport,
                                                                                         flags=flags)
                scapy.send(send_pkg, verbose=False)
        except Exception as e:
            loguru.logger.error(e)
    