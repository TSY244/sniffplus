# import socket
import MsgShare
import scapy.all as scapy
import loguru
import xTrace
'''
TCP forwarding
'''
'''
    从channel中获取TCP包，然后转发
'''


class TCPForwarding:
    def __init__(self, channel: MsgShare.Channel):
        self.channel = channel

    def forwarding(self):
        try:
            while True:
                # get the packet from the channel
                if self.channel.empty():
                    continue
                pkg = self.channel.pop()
                # get the five tuple of the packet
                sip, dip, sport, dport, flags = xTrace.MsgShare.get_five_tuple(pkg)
                # 使用scapy构造一个TCP包
                send_pkg = scapy.IP(src=sip, dst=dip) / scapy.TCP(sport=sport, dport=dport, flags=flags)

        except Exception as e:
            loguru.logger.error(e)
    