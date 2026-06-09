import asyncio
import sys
sys.path.append('/display')

from epaper_213_v4 import EPD_2in13_V4_Landscape
from display_frame import DisplayFrame, TextData, BYTE_ARRAY, TEXT, INSTRUCTIONS
from display_buffer import DisplayBuffer
from run_display import display_buffer

async def test_text_landscape():
    epd = EPD_2in13_V4_Landscape()

    buffer = DisplayBuffer()

    text_data = [
        TextData("Hello World", 0, 10),
        TextData("EPD Test", 0, 30),
    ]

    frame = DisplayFrame(
        type=TEXT,
        data=text_data,
        is_base=True
    )

    text_data_2 = [
        TextData("Hello World", 0, 10),
        TextData("EPD Test", 0, 30),
        TextData("Waga", 0, 50),
    ]

    frame_2 = DisplayFrame(
        type=TEXT,
        data=text_data_2,
    )

    buffer.add(frame, 1000)
    buffer.add(frame_2, 5000)

    await display_buffer(epd, buffer)

    epd.init()
    epd.Clear()
    epd.sleep()

asyncio.run(test_text_landscape())
