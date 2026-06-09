import utime

class DisplayBuffer():

    def __init__(self):
        self.buffer = []
        self.last_displayed = None

    def add(self, frame, delay):
        self.buffer.insert(0, (frame, delay))

    def check_ready_to_release(self):
        if self.last_displayed is None:
            return True

        next_buffer_item = self.buffer[-1]
        required_delay = next_buffer_item[1]

        delta_ms = utime.ticks_diff(utime.ticks_ms(), self.last_displayed)

        return delta_ms > required_delay

    def get_next(self):
        return self.buffer.pop()[0]

    def update_last_displayed(self):
        self.last_displayed = utime.ticks_ms()

    def get_buffer_run_time(self):
        from epaper_213_v4 import PARTIAL_REFRESH_TIME_MS

        num_frames = len(self.buffer)
        
        run_time = num_frames * PARTIAL_REFRESH_TIME_MS
        for frame in self.buffer:
            run_time += frame[1]

        return run_time