class FrameComponent:

    def draw_component(self, epd, colour):
        pass

class ByteArrayComponent(FrameComponent):
    def __init__(self, byte_array):
        self.byte_array = byte_array

    def draw_component(self, epd, colour):
        if colour == 0xFF:
            epd.buffer[:] = bytearray(b ^ 0xFF for b in self.byte_array)
        else:
            epd.buffer[:] = self.byte_array

class TextComponent(FrameComponent):
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y

    def draw_component(self, epd, colour):
        epd.text(self.text, self.x, self.y, colour)

class InstructionComponent(FrameComponent):

    PIXEL = 1
    HLINE = 2
    VLINE = 3
    LINE = 4
    RECT_EMPTY = 5
    RECT_FILLED = 6
    ELLIPSE_EMPTY = 7
    ELLIPSE_FILLED = 8
    POLYGON_EMPTY = 9
    POLYGON_FILLED = 10
    FILL = 11

    _PARAMS_MAPPING = {
        PIXEL : {'x', 'y'},
        HLINE: {'x', 'y', 'w'},
        VLINE: {'x', 'y', 'h'},
        LINE: {'x1', 'y1', 'x2', 'y2'},
        RECT_EMPTY: {'x', 'y', 'w', 'h'},
        RECT_FILLED: {'x', 'y', 'w', 'h'},
        ELLIPSE_EMPTY: {'x', 'y', 'xr', 'yr'},
        ELLIPSE_FILLED: {'x', 'y', 'xr', 'yr'},
        POLYGON_EMPTY: {'x', 'y', 'coords'},
        POLYGON_FILLED: {'x', 'y', 'coords'},
    }

    def __init__(self, component_type, filled=False, bitmask=None, **kwargs):

        if type != InstructionComponent.FILL:
            expected = InstructionComponent._PARAMS_MAPPING[type]
            if kwargs.keys() != expected:
                raise ValueError(f"Expected {expected}, got {set(kwargs.keys())}")
            
            if filled:
                kwargs['f'] = True

            if bitmask is not None:
                kwargs['m'] = bitmask

        self.component_type = component_type
        self.kwargs = kwargs


    def draw_component(self, epd, colour):
        if self.kwargs is not None:
            self.kwargs['c'] = colour

        match self.component_type:
            case InstructionComponent.PIXEL:
                epd.pixel(**self.kwargs)
            case InstructionComponent.HLINE:
                epd.hline(**self.kwargs)
            case InstructionComponent.VLINE:
                epd.vline(**self.kwargs)
            case InstructionComponent.LINE:
                epd.line(**self.kwargs)
            case InstructionComponent.RECT_EMPTY:
                epd.rect(**self.kwargs)
            case InstructionComponent.RECT_FILLED:
                epd.rect(**self.kwargs)
            case InstructionComponent.ELLIPSE_EMPTY:
                epd.ellipse(**self.kwargs)
            case InstructionComponent.ELLIPSE_FILLED:
                epd.ellipse(**self.kwargs)
            case InstructionComponent.POLYGON_EMPTY:
                epd.poly(**self.kwargs)
            case InstructionComponent.POLYGON_FILLED:
                epd.poly(**self.kwargs)
            case InstructionComponent.FILL:
                epd.fill(colour)