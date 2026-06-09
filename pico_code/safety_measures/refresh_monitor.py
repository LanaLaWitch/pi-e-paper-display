from datetime import datetime, timedelta

class RefreshMonitor():
    """ 
    The e-Paper display used recommends against images being retained for 24+ hours.
    This monitors the time since last refresh, so that we can clear the screen if controller fails.
    """

    def __init__(self, timeout_hours, min_refresh_wait):   
        self.timeout_hours = timeout_hours
        self.min_refresh_wait = min_refresh_wait
        self.last_refresh_time = datetime.now()
        self.timed_out = False

    def check_for_timeout(self):
        if self.timed_out:
            return True

        current_time = datetime.now()
        delta = current_time - self.last_refresh_time
        delta_seconds = timedelta.total_seconds(delta)
        delta_hours = delta_seconds / 3600

        timed_out = delta_hours > self.timeout_hours

        self.timed_out = timed_out
        return timed_out
    
    def check_past_min_refresh(self):
        current_time = datetime.now()
        delta = current_time - self.last_refresh_time
        delta_seconds = timedelta.total_seconds(delta)
        delta_minutes = delta_seconds * 60

        return delta_minutes >= self.min_refresh_wait

    
    def reset_monitor(self):
        """ Refresh request received. We can reset the monitor. """

        self.last_refresh_time = datetime.now()
        self.timed_out = False