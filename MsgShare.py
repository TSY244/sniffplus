import threading 
from multiprocessing import Queue

'''
used for sharing message between threads
'''


class Channel:
    def __init__(self):
        self.queue = []
        self.lock = threading.Lock()
    def put(self, item):
        '''
        args:
            item: data to be put into the queue
        '''
        with self.lock:
            self.queue.append(item)
    def top(self):
        '''
        return:
            the first element in the queue, but not pop it
        '''
        with self.lock:
            return self.queue[0]
    def pop(self):
        '''
        return:
            the first element in the queue, and pop it
        '''
        with self.lock:
            return self.queue.pop(0)
    def empty(self):
        '''
        return:
            True if the queue is empty, False otherwise
        '''
        with self.lock:
            return len(self.queue) == 0
    def size(self):
        '''
        return:
            the size of the queue
        '''
        with self.lock:
            return len(self.queue)
    def clear(self):
        with self.lock:
            self.queue = []
    def __str__(self):
        with self.lock:
            return str(self.queue)
        