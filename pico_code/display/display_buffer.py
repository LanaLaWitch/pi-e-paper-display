from collections import deque
from datetime import datetime, timedelta

class DisplayBuffer():

    def __init__(self):
        self.buffer = deque()
        self.last_displayed = None

    def add(self, frame, delay):
        self.buffer.appendleft((frame, delay))

    def check_ready_to_release(self):
        if self.last_displayed is None:
            return True
        
        next_buffer_item = self.buffer[-1]
        required_delay = next_buffer_item[1]

        current_time = datetime.now()
        delta = current_time - self.last_displayed
        delta_seconds = timedelta.total_seconds(delta)
        delta_milliseconds = delta_seconds * 1000

        return delta_milliseconds > required_delay
    
    def get_next(self):
        return self.buffer.pop()[0]
    
    def update_last_displayed(self):
        self.last_displayed = datetime.now()

    def get_buffer_run_time(self):
        from epaper_213_v4 import PARTIAL_REFRESH_TIME_MS

        num_frames = len(self.buffer)
        
        run_time = num_frames * PARTIAL_REFRESH_TIME_MS
        for frame in self.buffer:
            run_time += frame[1]

        return run_time