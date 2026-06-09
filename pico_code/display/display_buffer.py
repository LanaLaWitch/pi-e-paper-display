import utime

class DisplayBuffer():

    def __init__(self):
        self.buffer = []
        self.last_displayed = None

    def add(self, frame, delay):
        self.buffer.insert(0, (frame, delay))

    def get_next(self):
        return self.buffer.pop()

    def update_last_displayed(self):
        self.last_displayed = utime.ticks_ms()

    def get_buffer_run_time(self):
        from epaper_213_v4 import PARTIAL_REFRESH_TIME_MS

        num_frames = len(self.buffer)
        
        run_time = num_frames * PARTIAL_REFRESH_TIME_MS
        for frame in self.buffer:
            run_time += frame[1]

        return run_time