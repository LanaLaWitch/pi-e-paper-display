class DisplayFrame():

    def __init__(self, components, is_base=False, base_colour=0xFF):
        self.components = components
        self.is_base = is_base
        self.base_colour = base_colour

        # Draw colour is the opposite of the base colour
        self.draw_colour = base_colour ^ 0xFF

    def draw_frame(self, epd):
        if self.is_base:
            epd.fill(self.base_colour)

        for component in self.components:
            component.draw_component(epd, self.draw_colour)

        if self.is_base:
            epd.Display_Base(epd.buffer)
        else:
            epd.displayPartial(epd.buffer)