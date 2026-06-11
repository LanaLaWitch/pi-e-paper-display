import asyncio
import sys
sys.path.append('/display')

from epaper_213_v4 import EPD_2in13_V4_Landscape
from display_frame import DisplayFrame
from display_buffer import DisplayBuffer
from frame_components import TextComponent
from run_display import process_display_buffer

async def test_text_landscape():
    epd = EPD_2in13_V4_Landscape()

    buffer = DisplayBuffer()

    frame = DisplayFrame(
        components=[
            TextComponent("Hello World", 0, 10),
            TextComponent("EPD Test", 0, 30),
        ],
        is_base=True
    )

    frame_2 = DisplayFrame(
        components=[
            TextComponent("Hello World", 0, 10),
            TextComponent("EPD Test", 0, 30),
            TextComponent("Waga", 0, 50),
        ]
    )

    buffer.add(frame, 1000)
    buffer.add(frame_2, 5000)

    await process_display_buffer(epd, buffer)

    epd.init()
    epd.Clear()
    epd.sleep()

asyncio.run(test_text_landscape())
