import scapy.all as scapy
import loguru
import MsgShare
import threading
import socket
from time import sleep
'''
    Sniffer 
    This is a simple sniffer, which can only capture packets from a specific port.
    
'''
loguru.logger.add("log/sniffer_info.log", format="{time} {level} {message}", level="INFO", rotation="10 MB",
                  compression="zip")
loguru.logger.add("log/sniffer_error.log", format="{time} {level} {message}", level="ERROR", rotation="10 MB",
                  compression="zip")


class Sniffer:
    '''
        Impersonate a server and wait for connections.
    '''

    def __init__(self, ip,port, channel: MsgShare.Channel):
        self.port = port
        self.ip=ip
        self.channel = channel

    def sniff(self):
        '''
        sniff the packets from the specific port
        '''
        try:
            scapy.sniff(filter=f'tcp port {self.port}', iface='WLAN', count=0, prn=lambda x: self.channel.put(x))
        except Exception as e:
            loguru.logger.error(e)

    @staticmethod
    def get_local_ip():
        '''
        get the local ip address
        '''
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 
            s.connect(('8.8.8.8', 80)) 
            ip = s.getsockname()[0]
        except Exception as e:
            loguru.logger.error(e)
        finally:
            s.close()

    @staticmethod
    def tracert(pkg):
        '''
        trace the route of the packet
        '''
        sip, dip, sport, dport, flags = Sniffer.get_five_tuple(pkg)
        ack, seq = pkg['TCP'].ack, pkg['TCP'].seq
        send_pkg = scapy.IP(src=dip, dst=sip) / scapy.TCP(sport=dport, dport=sport, flags='R', ack=ack+1, seq=seq)
        for i in range(1, 128):
            # send the packet
            send_pkg.ttl = i
            ret = scapy.sr1(send_pkg, timeout=1, verbose=False)
            if ret == None or ret.src==sip:
                # print("route num is %d" % (i-1))
                loguru.logger.info(f"from {sip} to {dip} route num is {i-1}")
                break

    @staticmethod
    def get_five_tuple(pkg):
        '''
        get the five tuple of the packet
        pkg is a scapy packet
        '''
        try:
            ret = (pkg['IP'].src, pkg['IP'].dst, pkg['TCP'].sport, pkg['TCP'].dport, pkg['TCP'].flags)
        except Exception as e:
            loguru.logger.error(e)
        finally:
            return ret

    @staticmethod
    def get_mac(pkg):
        '''
        get the mac address of the packet
        pkg is a scapy packet
        '''
        try:
            ret = pkg['Ether'].src
        except Exception as e:
            loguru.logger.error(e)
        finally:
            return ret

# def main():
#     channel = MsgShare.Channel()
#     sniffer = Sniffer(Sniffer.get_local_ip(),80, channel)
#     thread_for_sniffer = threading.Thread(target=sniffer.sniff)
#     thread_for_sniffer.start()
#     while True:
#         if channel.empty():
#             continue
#         pkg = channel.top()
#         Sniffer.tracert(pkg)
#         sleep(1)

# if __name__ == "__main__":
#     main()
