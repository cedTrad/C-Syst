from threading import Thread, Lock, Condition, Event


class Synchrone:
    
    def __init__(self):
        self.x = 0