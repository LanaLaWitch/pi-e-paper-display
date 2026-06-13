import sys
sys.path.append('../..')

from controller_code.network.setup_sending_connection import establish_sending_connection
from controller_code.data_handling.build_packet import encode_packet
from shared.display.display_frame import DisplayFrame
from shared.display.frame_components import TextComponent, InstructionComponent

PORTRAIT = 1
WHITE = 0xFF
BLACK = 0x00

SUN_X = 61
SUN_Y = 60
SUN_RADIUS = 20
RAY_LENGTH = 10

def test_weather_display():
    print('Connecting to Pico...')
    sock = establish_sending_connection()

    frame = DisplayFrame(
        components=[
            # Sun body
            InstructionComponent(InstructionComponent.ELLIPSE_FILLED, BLACK, x=SUN_X, y=SUN_Y, xr=SUN_RADIUS, yr=SUN_RADIUS),

            # Sun rays - N, S, E, W
            InstructionComponent(InstructionComponent.VLINE, BLACK, x=SUN_X, y=SUN_Y - SUN_RADIUS - RAY_LENGTH, h=RAY_LENGTH),
            InstructionComponent(InstructionComponent.VLINE, BLACK, x=SUN_X, y=SUN_Y + SUN_RADIUS, h=RAY_LENGTH),
            InstructionComponent(InstructionComponent.HLINE, BLACK, x=SUN_X - SUN_RADIUS - RAY_LENGTH, y=SUN_Y, w=RAY_LENGTH),
            InstructionComponent(InstructionComponent.HLINE, BLACK, x=SUN_X + SUN_RADIUS, y=SUN_Y, w=RAY_LENGTH),

            # Sun rays - diagonals
            InstructionComponent(InstructionComponent.LINE, BLACK, x1=SUN_X - 15, y1=SUN_Y - 15, x2=SUN_X - 22, y2=SUN_Y - 22),
            InstructionComponent(InstructionComponent.LINE, BLACK, x1=SUN_X + 15, y1=SUN_Y - 15, x2=SUN_X + 22, y2=SUN_Y - 22),
            InstructionComponent(InstructionComponent.LINE, BLACK, x1=SUN_X - 15, y1=SUN_Y + 15, x2=SUN_X - 22, y2=SUN_Y + 22),
            InstructionComponent(InstructionComponent.LINE, BLACK, x1=SUN_X + 15, y1=SUN_Y + 15, x2=SUN_X + 22, y2=SUN_Y + 22),

            # Weather text
            TextComponent('Sunny', 35, 100, BLACK),
            TextComponent('Temp:  21 C', 10, 130, BLACK),
            TextComponent('Humid: 45%', 10, 150, BLACK),
            TextComponent('Wind:  12 km/h', 10, 170, BLACK),
        ],
        is_base=True,
        base_colour=WHITE
    )

    packet = encode_packet([(frame, 30000)], bg_colour=WHITE, orientation=PORTRAIT)

    print(f'Sending packet ({len(packet)} bytes)...')
    sock.sendall(packet)
    print('Sent successfully')

    sock.close()

test_weather_display()
