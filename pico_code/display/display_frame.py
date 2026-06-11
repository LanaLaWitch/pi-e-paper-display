class DisplayFrame():

    def __init__(self, components, is_base=False, base_colour=0xFF):
        self.components = components
        self.is_base = is_base
        self.base_colour = base_colour

    def draw_frame(self, epd):
        if self.is_base:
            epd.fill(self.base_colour)

        for component in self.components:
            component.draw_component(epd)

        if self.is_base:
            epd.Display_Base(epd.buffer)
        else:
            epd.displayPartial(epd.buffer)