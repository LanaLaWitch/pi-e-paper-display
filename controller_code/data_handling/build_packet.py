import struct
from shared.display.frame_components import FrameComponent, InstructionComponent

def encode_packet(display_frames, bg_colour, orientation):
    data_packet = struct.pack('>B', len(display_frames))
    data_packet += struct.pack('>B', bg_colour)
    data_packet += struct.pack('>B', orientation)

    for frame in display_frames:

        display_frame = frame[0]

        data_packet += struct.pack('>I', frame[1])
        data_packet += struct.pack('>B', len(display_frame.components))

        for component in display_frame.components:

            data_packet += struct.pack('>B', component.component_type)
            data_packet += struct.pack('>B', component.colour)

            match component.component_type:
                case FrameComponent.BYTE_ARRAY:
                    component_data_packet = component.byte_array
                case FrameComponent.TEXT:
                    component_data_packet = _encode_text_component(component)
                case FrameComponent.INSTRUCTION:
                    component_data_packet = _encode_instruction_component(component)

            data_packet += struct.pack('>I', len(component_data_packet))
            data_packet += component_data_packet

    return data_packet


def _encode_text_component(component):
    temp_packet = struct.pack('>H', component.x)
    temp_packet += struct.pack('>H', component.y)
    temp_packet += component.text.encode('utf-8')

    return temp_packet


def _encode_instruction_component(component):
    temp_packet = struct.pack('>B', component.instruction_type)

    match component.instruction_type:
        case InstructionComponent.PIXEL:
            temp_packet += struct.pack('>H', component.kwargs['x'])
            temp_packet += struct.pack('>H', component.kwargs['y'])
        case InstructionComponent.HLINE:
            temp_packet += struct.pack('>H', component.kwargs['x'])
            temp_packet += struct.pack('>H', component.kwargs['y'])
            temp_packet += struct.pack('>H', component.kwargs['w'])
        case InstructionComponent.VLINE:
            temp_packet += struct.pack('>H', component.kwargs['x'])
            temp_packet += struct.pack('>H', component.kwargs['y'])
            temp_packet += struct.pack('>H', component.kwargs['h'])
        case InstructionComponent.LINE:
            temp_packet += struct.pack('>H', component.kwargs['x1'])
            temp_packet += struct.pack('>H', component.kwargs['y1'])
            temp_packet += struct.pack('>H', component.kwargs['x2'])
            temp_packet += struct.pack('>H', component.kwargs['y2'])
        case InstructionComponent.RECT_EMPTY | InstructionComponent.RECT_FILLED:
            temp_packet += struct.pack('>H', component.kwargs['x'])
            temp_packet += struct.pack('>H', component.kwargs['y'])
            temp_packet += struct.pack('>H', component.kwargs['w'])
            temp_packet += struct.pack('>H', component.kwargs['h'])
        case InstructionComponent.ELLIPSE_EMPTY | InstructionComponent.ELLIPSE_FILLED:
            temp_packet += struct.pack('>H', component.kwargs['x'])
            temp_packet += struct.pack('>H', component.kwargs['y'])
            temp_packet += struct.pack('>H', component.kwargs['xr'])
            temp_packet += struct.pack('>H', component.kwargs['yr'])
            if 'm' in component.kwargs:
                temp_packet += struct.pack('>B', component.kwargs['m'])
        case InstructionComponent.POLYGON_EMPTY | InstructionComponent.POLYGON_FILLED:
            temp_packet += struct.pack('>H', component.kwargs['x'])
            temp_packet += struct.pack('>H', component.kwargs['y'])
            temp_packet += _encode_coords(component.kwargs['coords'])
    return temp_packet


def _encode_coords(coords):
    data = b''
    for coord in coords:
        data += struct.pack('>h', coord)
    return data