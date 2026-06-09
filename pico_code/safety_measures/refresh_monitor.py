from datetime import datetime, timedelta

class RefreshMonitor():

    def __init__(self, timeout_hours):    
        self.timeout_hours = timeout_hours
        self.last_refresh_time = datetime.now()
        self.timed_out = False

    def check_for_timeout(self):

        if self.timed_out:
            return True

        current_time = datetime.now()
        delta = current_time - self.last_refresh_time
        delta_seconds = timedelta.total_seconds(delta)
        delta_hours = delta_seconds / 3600

        timed_out = delta_seconds > self.timeout_hours

        self.timed_out = timed_out
        return timed_out
    
    def reset_monitor(self):
        """ Refresh request received. We can reset the monitor. """

        self.last_refresh_time = datetime.now()
        self.timed_out = False