import time

class Clock:
    def __init__(self):
        self.start_time = time.time()
        self.current_time = time.time()

    def get_time(self):
        return time.time() - self.start_time

    def get_dt(self):
        return time.time() - self.current_time

    def update(self):
        self.current_time = time.time()

    def delay(self, sec):
        time.sleep(sec)

class Timer:
    def __init__(self):
        self.count = 0

    def set_timer(self, sec):
        self.count = sec
    
    def update(self, dt):
        if self.count > 0:
            self.count -= dt
            
