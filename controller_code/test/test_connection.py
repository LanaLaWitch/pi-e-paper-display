import sys
sys.path.append('../..')

from controller_code.network.setup_sending_connection import establish_sending_connection
from controller_code.data_handling.build_packet import encode_packet
from shared.display.display_frame import DisplayFrame
from shared.display.frame_components import TextComponent

PORTRAIT = 1
WHITE = 0xFF
BLACK = 0x00

def test_send_display():
    print('Connecting to Pico...')
    sock = establish_sending_connection()

    frame = DisplayFrame(
        components=[
            TextComponent('Hello Pico!', 0, 10, BLACK),
            TextComponent('Test image', 0, 30, BLACK),
        ],
        is_base=True,
        base_colour=WHITE
    )

    packet = encode_packet([(frame, 5000)], bg_colour=WHITE, orientation=PORTRAIT)

    print(f'Sending packet ({len(packet)} bytes)...')
    sock.sendall(packet)
    print('Sent successfully')

    sock.close()

test_send_display()
