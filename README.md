# 简介
本项目一共有四个功能 

> TCP_forwarding.py :
>
> 负责：tcp 代理  监听转口，监听IP，转发端口，转发端口
>
> TCP转发，进程间通信xtarcet

> sniffer.py:
>
> 主要工作是负责嗅探，主要是获取五元组
>
> 源IP，源端口，目的IP，目的端口
>
> 获取到了信息之后将其存放到队列里面

> thread_channel.py:
>
> 主要用于五元组信息的传输

> arpspoof.py:
>
> 用于arp欺骗
>
> 需要 目标IP 目标MAC 网关IP 网关MAC

# 使用
需要填写欺骗的服务器的ip
您需要在main.py处将
`# target_ip, target_mac = #!!input the target ip and mac`
取消注释，然后填写ip，我会根据这个获取该服务器的mac，随后我将对其进行arp欺骗
