import scapy.all as scapy
import socket
import MsgShare

class ArpSpoof:
    '''
        Impersonate a server and wait for connections.
    '''
    def __init__(self,channel:MsgShare.Channel):
        self.channel=channel
        
        
