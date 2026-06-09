from enum import Enum

class DisplayFrameType(Enum):
    BYTE_ARRAY = 1
    TEXT = 2
    INSTRUCTIONS = 3

class TextData:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y

class DisplayFrame():
    def __init__(self, type, data, is_base=False, base_colour=0xFF):
        self.type = type
        self.data = data
        self.is_base = is_base
        self.base_colour = base_colour

        if base_colour == 0xFF:
            self.draw_colour = 0x00
        else:
            self.draw_colour = 0xFF

    def get_draw_function(self):
        if self.type == DisplayFrameType.BYTE_ARRAY:
            return self._draw_func_byte_array
        elif self.type == DisplayFrameType.TEXT:
            return self._draw_func_text
        elif self.type == DisplayFrameType.INSTRUCTIONS:
            return self._draw_func_instructions
        else:
            raise ValueError("Unknown DisplayFrameType: {}".format(self.type))

    def _draw_func_byte_array(self, epd):
        if self.base_colour == 0xFF:
            epd.buffer[:] = self.data
        else:
            epd.buffer[:] = bytearray(b ^ 0xFF for b in self.data)
        if self.is_base:
            epd.Display_Base(epd.buffer)
        else:
            epd.displayPartial(epd.buffer)

    def _draw_func_text(self, epd):
        epd.fill(self.base_colour)
        if isinstance(self.data, list):
            for item in self.data:
                epd.text(item.text, item.x, item.y, self.draw_colour)
        else:
            epd.text(self.data.text, self.data.x, self.data.y, self.draw_colour)
        if self.is_base:
            epd.Display_Base(epd.buffer)
        else:
            epd.displayPartial(epd.buffer)

    def _draw_func_instructions(self, epd):
        # TODO: implement instructions rendering
        pass
