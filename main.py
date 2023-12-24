import TcpRelkay


def main():
    # init the channel
    channel = TcpRelkay.Channel()
    # init the tcp forwarding
    tcp_forwarding = TcpRelkay.TCPForwarding(channel)