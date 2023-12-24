import socket
import scapy.all as scapy
import loguru
import MsgShare
import threading
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

    def __init__(self, port, channel: MsgShare.Channel):
        self.port = port
        try:
            # self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
            self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.socket.bind(('127.0.0.1', self.port))
            self.socket.listen(1)
            # self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)  # open the promiscuous mode
        except Exception as e:
            loguru.logger.error(e)
        self.channel = channel

    def socket_accept(self):
        '''
        accept the connection
        '''
        try:
            self.socket.accept()
        except Exception as e:
            loguru.logger.error(e)
    def get_host_ip(self):
        """
        find the ip address of the host
        return: ip
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except Exception as e:
            loguru.logger.error(e)
        finally:
            s.close()
        return ip

    def sniff(self):
        '''
        
        sniff the packets from the specific port
        '''
        try:
            while True:

                # use scapy to parse the packet
                pkg = scapy.sniff(filter=f'tcp port {self.port}',iface='WLAN',count=0,prn=self.callback)
        except Exception as e:
            loguru.logger.error(e)
        finally:
            # self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)  # close the promiscuous mode
            self.socket.close()

    def callback(self,pkg):
        self.channel.put(pkg)
        print(pkg)
    @staticmethod
    def tracert(self, pkg):
        '''
        trace the route of the packet
        '''
        sip, dip, sport, dport, flags = self.get_five_tuple(pkg)
        ack, seq = pkg['TCP'].ack, pkg['TCP'].seq
        send_pkg = scapy.IP(src=dip, dst=sip) / scapy.TCP(sport=dport, dport=sport, flags='R', ack=ack, seq=seq)
        for i in range(1, 128):
            # send the packet
            ret = scapy.sr1(send_pkg, timeout=1)
            if ret is None:
                loguru.logger.info("the " + str(i) + "th hop is " + str(dip))
                break
            elif ret['IP'].src == dip:
                loguru.logger.info("the " + str(i) + "th hop is " + str(dip))
                break
            else:
                loguru.logger.info("the " + str(i) + "th hop is " + str(ret['IP'].src))
                continue

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


def sniffer():
    scapy.sniff(filter=f'tcp',iface='WLAN',count=0,prn=lambda x:print(x))

sniffer()
# def main():
#     channel = MsgShare.Channel()
#     ac_thread=threading.Thread(target=Sniffer.socket_accept)
#     ac_thread.start()
#     sniffer = Sniffer(11234, channel)
#     sniffer.sniff()


# if __name__ == "__main__":
#     main()
