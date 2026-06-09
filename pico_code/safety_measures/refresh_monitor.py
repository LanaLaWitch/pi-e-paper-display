import utime

class RefreshMonitor():
    """
    The e-Paper display used recommends against images being retained for 24+ hours.
    This monitors the time since last refresh, so that we can clear the screen if controller fails.
    """

    def __init__(self, timeout_hours, min_refresh_wait):
        self.timeout_hours = timeout_hours
        self.min_refresh_wait = min_refresh_wait
        self.last_refresh_time = utime.ticks_ms()
        self.timed_out = False

    def check_for_timeout(self):
        if self.timed_out:
            return True

        delta_ms = utime.ticks_diff(utime.ticks_ms(), self.last_refresh_time)
        delta_hours = delta_ms / 3_600_000

        self.timed_out = delta_hours > self.timeout_hours
        return self.timed_out

    def check_past_min_refresh(self):
        delta_ms = utime.ticks_diff(utime.ticks_ms(), self.last_refresh_time)
        delta_minutes = delta_ms / 60_000

        return delta_minutes >= self.min_refresh_wait

    def reset_monitor(self):
        """ Refresh request received. We can reset the monitor. """

        self.last_refresh_time = utime.ticks_ms()
        self.timed_out = False