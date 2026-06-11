from display_buffer import DisplayBuffer
from display_frame import DisplayFrame
from frame_components import FrameComponent, ByteArrayComponent, TextComponent, InstructionComponent
from array import array


async def get_display_frame_buffer(conn):
    decoded_frames = await _decode_packet(conn)
    return DisplayBuffer(decoded_frames)


async def _read(conn, n):
    buffer = bytearray(n)
    view = memoryview(buffer)
    received = 0
    while received < n:
        chunk = conn.recv(n - received)
        if chunk:
            view[received:received + len(chunk)] = chunk
            received += len(chunk)
    return buffer


async def _decode_packet(conn):
    frame_count = int.from_bytes(await _read(conn, 1), 'big')
    bg_colour = int.from_bytes(await _read(conn, 1), 'big')

    frames = []
    is_base_frame = True
    for _ in range(frame_count):

        delay_ms = int.from_bytes(await _read(conn, 4), 'big')
        component_count = int.from_bytes(await _read(conn, 1), 'big')

        components = []
        for _ in range(component_count):

            component_type = int.from_bytes(await _read(conn, 1), 'big')
            draw_colour = int.from_bytes(await _read(conn, 1), 'big')
            data_length = int.from_bytes(await _read(conn, 4), 'big')

            component_data = await _read(conn, data_length)
            match component_type:
                case FrameComponent.BYTE_ARRAY:
                    components.append(ByteArrayComponent(bytes(component_data), draw_colour))
                case FrameComponent.TEXT:
                    components.append(_decode_text_component(component_data, draw_colour))
                case FrameComponent.INSTRUCTION:
                    components.append(_decode_instruction_component(component_data, draw_colour))

        frame_object = DisplayFrame(components, is_base_frame, bg_colour)
        frames.append((frame_object, delay_ms))
        is_base_frame = False

    return frames


def _decode_text_component(data, draw_colour):
    x = int.from_bytes(data[0:2], 'big')
    y = int.from_bytes(data[2:4], 'big')
    text = data[4:].decode('utf-8')

    return TextComponent(text, x, y, draw_colour)


def _decode_instruction_component(data, draw_colour):
    instruction_type = int.from_bytes(data[0:1], 'big')

    match instruction_type:
        case InstructionComponent.FILL:
            return InstructionComponent(InstructionComponent.FILL, draw_colour)
        case InstructionComponent.PIXEL:
            x = int.from_bytes(data[1:3], 'big')
            y = int.from_bytes(data[3:5], 'big')
            return InstructionComponent(InstructionComponent.PIXEL, draw_colour, x=x, y=y)
        case InstructionComponent.HLINE:
            x = int.from_bytes(data[1:3], 'big')
            y = int.from_bytes(data[3:5], 'big')
            w = int.from_bytes(data[5:7], 'big')
            return InstructionComponent(InstructionComponent.HLINE, draw_colour, x=x, y=y, w=w)
        case InstructionComponent.VLINE:
            x = int.from_bytes(data[1:3], 'big')
            y = int.from_bytes(data[3:5], 'big')
            h = int.from_bytes(data[5:7], 'big')
            return InstructionComponent(InstructionComponent.VLINE, draw_colour, x=x, y=y, h=h)
        case InstructionComponent.LINE:
            x1 = int.from_bytes(data[1:3], 'big')
            y1 = int.from_bytes(data[3:5], 'big')
            x2 = int.from_bytes(data[5:7], 'big')
            y2 = int.from_bytes(data[7:9], 'big')
            return InstructionComponent(InstructionComponent.LINE, draw_colour, x1=x1, y1=y1, x2=x2, y2=y2)
        case InstructionComponent.RECT_EMPTY:
            x = int.from_bytes(data[1:3], 'big')
            y = int.from_bytes(data[3:5], 'big')
            w = int.from_bytes(data[5:7], 'big')
            h = int.from_bytes(data[7:9], 'big')
            return InstructionComponent(InstructionComponent.RECT_EMPTY, draw_colour, x=x, y=y, w=w, h=h)
        case InstructionComponent.RECT_FILLED:
            x = int.from_bytes(data[1:3], 'big')
            y = int.from_bytes(data[3:5], 'big')
            w = int.from_bytes(data[5:7], 'big')
            h = int.from_bytes(data[7:9], 'big')
            return InstructionComponent(InstructionComponent.RECT_FILLED, draw_colour, filled=True, x=x, y=y, w=w, h=h)
        case InstructionComponent.ELLIPSE_EMPTY:
            x = int.from_bytes(data[1:3], 'big')
            y = int.from_bytes(data[3:5], 'big')
            xr = int.from_bytes(data[5:7], 'big')
            yr = int.from_bytes(data[7:9], 'big')
            bitmask = int.from_bytes(data[9:10], 'big') if len(data) > 9 else None
            return InstructionComponent(InstructionComponent.ELLIPSE_EMPTY, draw_colour, bitmask=bitmask, x=x, y=y, xr=xr, yr=yr)
        case InstructionComponent.ELLIPSE_FILLED:
            x = int.from_bytes(data[1:3], 'big')
            y = int.from_bytes(data[3:5], 'big')
            xr = int.from_bytes(data[5:7], 'big')
            yr = int.from_bytes(data[7:9], 'big')
            bitmask = int.from_bytes(data[9:10], 'big') if len(data) > 9 else None
            return InstructionComponent(InstructionComponent.ELLIPSE_FILLED, draw_colour, filled=True, bitmask=bitmask, x=x, y=y, xr=xr, yr=yr)
        case InstructionComponent.POLYGON_EMPTY:
            x = int.from_bytes(data[1:3], 'big')
            y = int.from_bytes(data[3:5], 'big')
            coords = _decode_coords(data[5:])
            return InstructionComponent(InstructionComponent.POLYGON_EMPTY, draw_colour, x=x, y=y, coords=coords)
        case InstructionComponent.POLYGON_FILLED:
            x = int.from_bytes(data[1:3], 'big')
            y = int.from_bytes(data[3:5], 'big')
            coords = _decode_coords(data[5:])
            return InstructionComponent(InstructionComponent.POLYGON_FILLED, draw_colour, filled=True, x=x, y=y, coords=coords)


def _decode_coords(coords_slice):
    coords = array('h')
    for i in range(0, len(coords_slice), 2):
        coords.append(int.from_bytes(coords_slice[i:i+2], 'big'))
    return coords
