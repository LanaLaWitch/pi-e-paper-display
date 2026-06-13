import sys
sys.path.append('../..')

from controller_code.network.setup_sending_connection import establish_sending_connection
from controller_code.data_handling.build_packet import encode_packet
from shared.display.display_frame import DisplayFrame
from shared.display.frame_components import InstructionComponent

PORTRAIT = 1
WHITE = 0xFF

def test_clear_display():
    print('Connecting to Pico...')
    sock = establish_sending_connection()

    frame = DisplayFrame(
        components=[
            InstructionComponent(InstructionComponent.FILL, WHITE),
        ],
        is_base=True,
        base_colour=WHITE
    )

    packet = encode_packet([(frame, 0)], bg_colour=WHITE, orientation=PORTRAIT)

    print(f'Sending clear packet ({len(packet)} bytes)...')
    sock.sendall(packet)
    print('Cleared successfully')

    sock.close()

test_clear_display()
