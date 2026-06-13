from pico_code.display.epaper_213_v4 import EPD_2in13_V4_Portrait

def clear_epd_display():

    # Clearing screen so the orientation won't matter
    epd = EPD_2in13_V4_Portrait()

    epd.init()
    epd.Clear()
    epd.sleep()