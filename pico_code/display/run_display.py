from display_buffer import DisplayBuffer
from datetime import datetime, timedelta

def display_buffer(epd, buffer: DisplayBuffer):

    epd.init()
    epd.Clear()

    # To ensure we exit the loop, we'll look at the expected run time and add 5 seconds
    expected_run_time = buffer.get_buffer_run_time()
    forgiving_run_time = expected_run_time + 5000
    starting_datetime = datetime.now()

    while len(buffer.buffer) > 0:
        if check_timeout(forgiving_run_time, starting_datetime):
            break

        if not buffer.check_ready_to_release():
            continue
        
        frame = buffer.get_next()
        draw_func = frame.get_draw_function()
        draw_func(epd)

    epd.sleep()

def check_timeout(max_run_time, initial_datetime):
    current_time = datetime.now()
    delta = current_time - initial_datetime
    delta_seconds = timedelta.total_seconds(delta)
    delta_milliseconds = delta_seconds * 1000

    return delta_milliseconds > max_run_time