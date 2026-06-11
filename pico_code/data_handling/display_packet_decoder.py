from display_buffer import DisplayBuffer
from display_frame import DisplayFrame
from frame_components import FrameComponent, ByteArrayComponent, TextComponent, InstructionComponent
from array import array


def get_display_frame_buffer(data_packet):
    decoded_frames = _decode_packet(data_packet)
    return DisplayBuffer(decoded_frames)


def _decode_packet(data_packet):
    frame_count = int.from_bytes(data_packet[0:1], 'big')
    bg_colour = int.from_bytes(data_packet[1:2], 'big')

    frames = []
    is_base_frame = True
    fsi = 2
    for frame in range(frame_count):

        delay_ms = int.from_bytes(data_packet[fsi:fsi+4], 'big')
        component_count = int.from_bytes(data_packet[fsi+4:fsi+5], 'big')

        components = []
        csi = fsi+5
        for component in range(component_count):

            component_type = int.from_bytes(data_packet[csi:csi+1], 'big')
            draw_colour = int.from_bytes(data_packet[csi+1:csi+2], 'big')
            data_length = int.from_bytes(data_packet[csi+2:csi+6], 'big')

            start_of_next_component_ind = csi + 6 + data_length

            component_data_slice = data_packet[csi+6:start_of_next_component_ind]
            match component_type:
                case FrameComponent.BYTE_ARRAY:
                    components.append(ByteArrayComponent(bytes(component_data_slice), draw_colour))
                case FrameComponent.TEXT:
                    components.append(_decode_text_packet_slice(component_data_slice, draw_colour))
                case FrameComponent.INSTRUCTION:
                    components.append(_decode_instruction_packet_slice(component_data_slice, draw_colour))

            csi = start_of_next_component_ind

        frame_object = DisplayFrame(components, is_base_frame, bg_colour)
        frames.append((frame_object, delay_ms))
        is_base_frame = False
        fsi = csi

    return frames


def _decode_text_packet_slice(packet_slice, draw_colour):
    x = int.from_bytes(packet_slice[0:2], 'big')
    y = int.from_bytes(packet_slice[2:4], 'big')
    text = packet_slice[4:].decode('utf-8')

    return TextComponent(text, x, y, draw_colour)


def _decode_instruction_packet_slice(packet_slice, draw_colour):
    instruction_type = int.from_bytes(packet_slice[0:1], 'big')

    match instruction_type:
        case InstructionComponent.FILL:
            return InstructionComponent(InstructionComponent.FILL, draw_colour)
        case InstructionComponent.PIXEL:
            x = int.from_bytes(packet_slice[1:3], 'big')
            y = int.from_bytes(packet_slice[3:5], 'big')
            return InstructionComponent(InstructionComponent.PIXEL, draw_colour, x=x, y=y)
        case InstructionComponent.HLINE:
            x = int.from_bytes(packet_slice[1:3], 'big')
            y = int.from_bytes(packet_slice[3:5], 'big')
            w = int.from_bytes(packet_slice[5:7], 'big')
            return InstructionComponent(InstructionComponent.HLINE, draw_colour, x=x, y=y, w=w)
        case InstructionComponent.VLINE:
            x = int.from_bytes(packet_slice[1:3], 'big')
            y = int.from_bytes(packet_slice[3:5], 'big')
            h = int.from_bytes(packet_slice[5:7], 'big')
            return InstructionComponent(InstructionComponent.VLINE, draw_colour, x=x, y=y, h=h)
        case InstructionComponent.LINE:
            x1 = int.from_bytes(packet_slice[1:3], 'big')
            y1 = int.from_bytes(packet_slice[3:5], 'big')
            x2 = int.from_bytes(packet_slice[5:7], 'big')
            y2 = int.from_bytes(packet_slice[7:9], 'big')
            return InstructionComponent(InstructionComponent.LINE, draw_colour, x1=x1, y1=y1, x2=x2, y2=y2)
        case InstructionComponent.RECT_EMPTY:
            x = int.from_bytes(packet_slice[1:3], 'big')
            y = int.from_bytes(packet_slice[3:5], 'big')
            w = int.from_bytes(packet_slice[5:7], 'big')
            h = int.from_bytes(packet_slice[7:9], 'big')
            return InstructionComponent(InstructionComponent.RECT_EMPTY, draw_colour, x=x, y=y, w=w, h=h)
        case InstructionComponent.RECT_FILLED:
            x = int.from_bytes(packet_slice[1:3], 'big')
            y = int.from_bytes(packet_slice[3:5], 'big')
            w = int.from_bytes(packet_slice[5:7], 'big')
            h = int.from_bytes(packet_slice[7:9], 'big')
            return InstructionComponent(InstructionComponent.RECT_FILLED, draw_colour, filled=True, x=x, y=y, w=w, h=h)
        case InstructionComponent.ELLIPSE_EMPTY:
            x = int.from_bytes(packet_slice[1:3], 'big')
            y = int.from_bytes(packet_slice[3:5], 'big')
            xr = int.from_bytes(packet_slice[5:7], 'big')
            yr = int.from_bytes(packet_slice[7:9], 'big')
            bitmask = int.from_bytes(packet_slice[9:10], 'big') if len(packet_slice) > 9 else None
            return InstructionComponent(InstructionComponent.ELLIPSE_EMPTY, draw_colour, bitmask=bitmask, x=x, y=y, xr=xr, yr=yr)
        case InstructionComponent.ELLIPSE_FILLED:
            x = int.from_bytes(packet_slice[1:3], 'big')
            y = int.from_bytes(packet_slice[3:5], 'big')
            xr = int.from_bytes(packet_slice[5:7], 'big')
            yr = int.from_bytes(packet_slice[7:9], 'big')
            bitmask = int.from_bytes(packet_slice[9:10], 'big') if len(packet_slice) > 9 else None
            return InstructionComponent(InstructionComponent.ELLIPSE_FILLED, draw_colour, filled=True, bitmask=bitmask, x=x, y=y, xr=xr, yr=yr)
        case InstructionComponent.POLYGON_EMPTY:
            x = int.from_bytes(packet_slice[1:3], 'big')
            y = int.from_bytes(packet_slice[3:5], 'big')
            coords = _decode_coords(packet_slice[5:])
            return InstructionComponent(InstructionComponent.POLYGON_EMPTY, draw_colour, x=x, y=y, coords=coords)
        case InstructionComponent.POLYGON_FILLED:
            x = int.from_bytes(packet_slice[1:3], 'big')
            y = int.from_bytes(packet_slice[3:5], 'big')
            coords = _decode_coords(packet_slice[5:])
            return InstructionComponent(InstructionComponent.POLYGON_FILLED, draw_colour, filled=True, x=x, y=y, coords=coords)


def _decode_coords(coords_slice):
    coords = array('h')
    for i in range(0, len(coords_slice), 2):
        coords.append(int.from_bytes(coords_slice[i:i+2], 'big'))
    return coords
