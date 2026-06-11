from display_buffer import DisplayBuffer
import utime
import asyncio

async def process_display_buffer(epd, buffer: DisplayBuffer):

    epd.init()
    epd.Clear()

    # To ensure we exit the loop, we'll look at the expected run time and add 5 seconds
    expected_run_time = buffer.get_buffer_run_time()
    forgiving_run_time = expected_run_time + 5000
    start_ticks = utime.ticks_ms()

    while len(buffer.buffer) > 0:
        if check_timeout(forgiving_run_time, start_ticks):
            break

        frame, delay = buffer.get_next()

        draw_func = frame.draw_frame(epd)
        draw_func(epd)

        await asyncio.sleep_ms(delay)

    epd.sleep()

def check_timeout(max_run_time, start_ticks):
    delta_ms = utime.ticks_diff(utime.ticks_ms(), start_ticks)
    return delta_ms > max_run_time