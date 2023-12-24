import uuid

def get_mac_address():
    mac=uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])

print(get_mac_address())

# import socket

# def get_host_ip():
#     """
#     查询本机ip地址
#     :return: ip
#     """
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # 
#         s.connect(('8.8.8.8', 80)) # 
#         ip = s.getsockname()[0] # 
#     finally:
#         s.close()

#     return ip

# if __name__ == '__main__':
#     print(get_host_ip())


# import threading, time

# class Hider(threading.Thread):
#     def __init__(self, cond, name):
#         super(Hider, self).__init__()
#         self.cond = cond
#         self.name = name

#     def run(self):
#         time.sleep(1)  #确保先运行Seeker中的方法
#         self.cond.acquire()

#         print(self.name + ': 我已经把眼睛蒙上了')
#         self.cond.notify()
#         self.cond.wait()
#         print(self.name + ': 我找到你了哦 ~_~')
#         self.cond.notify() 

#         self.cond.release()
#         print(self.name + ': 我赢了')

# class Seeker(threading.Thread):
#     def __init__(self, cond, name):
#         super(Seeker, self).__init__()
#         self.cond = cond
#         self.name = name

#     def run(self):
#         self.cond.acquire()
#         self.cond.wait()
#         print(self.name + ': 我已经藏好了，你快来找我吧')
#         self.cond.notify()
#         self.cond.wait()
#         self.cond.release()
#         print(self.name + ': 被你找到了，哎~~~')

# cond = threading.Condition()
# seeker = Seeker(cond, 'seeker')
# hider = Hider(cond, 'hider')
# seeker.start()
# hider.start()