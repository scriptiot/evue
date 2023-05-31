# -*- coding: utf-8 -*-
from loguru import logger
from math import pi
from typing import Optional
from flet import Control, Container, border, margin, padding, border_radius,  DragUpdateEvent, GestureDetector
from beartype import beartype

class BaseContainer(Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bgcolor = "transparent"
        self.margin_left = 0
        self.margin_top = 0
        self.margin_right = 0
        self.margin_bottom = 0
        self.padding_left = 0
        self.padding_top = 0
        self.padding_right = 0
        self.padding_bottom = 0

        self.border_left = 0
        self.border_left_color = bgcolor
        self.border_top = 0
        self.border_top_color = bgcolor
        self.border_right = 0
        self.border_right_color = bgcolor
        self.border_bottom = 0
        self.border_bottom_color = bgcolor
        self.border_color = 0
        self.border_radius = 0
        self.border_radius_topLeft = 0
        self.border_radius_topRight = 0
        self.border_radius_bottomLeft = 0
        self.border_radius_bottomRight = 0

    def updateMargin(self):
        self.margin = margin.only(left=self.margin_left, 
                                  top=self.margin_top, 
                                  right=self.margin_right,
                                  bottom=self.margin_bottom
                                )

    def set_margin(self, value):
        value = int(value)
        self.margin_left = value
        self.margin_top = value
        self.margin_right = value
        self.margin_bottom = value
        self.updateMargin()

    def set_margin_left(self, value):
        value = int(value)
        self.margin_left = value
        self.updateMargin()

    def set_margin_top(self, value):
        value = int(value)
        self.margin_top = value
        self.updateMargin()

    def set_margin_right(self, value):
        value = int(value)
        self.margin_right = value
        self.updateMargin()

    def set_margin_bottom(self, value):
        value = int(value)
        self.margin_bottom = value
        self.updateMargin()

    def updatePadding(self):
        self.padding = padding.only(left=self.padding_left, 
                                  top=self.padding_top, 
                                  right=self.padding_right,
                                  bottom=self.padding_bottom
                                )

    def set_padding(self, value):
        value = int(value)
        self.padding_left = value
        self.padding_top = value
        self.padding_right = value
        self.padding_bottom = value
        self.updatePadding()

    def set_padding_left(self, value):
        value = int(value)
        self.padding_left = value
        self.updatePadding()

    def set_padding_top(self, value):
        value = int(value)
        self.padding_top = value
        self.updatePadding()

    def set_padding_right(self, value):
        value = int(value)
        self.padding_right = value
        self.updatePadding()

    def set_padding_bottom(self, value):
        value = int(value)
        self.padding_bottom = value
        self.updatePadding()

    def updateBorder(self):
        self.border = border.only(border.BorderSide(self.border_left, self.border_left_color),
                    border.BorderSide(self.border_top, self.border_top_color),
                    border.BorderSide(self.border_right, self.border_right_color),
                    border.BorderSide(self.border_bottom, self.border_bottom_color))

    def updateBorderRadius(self):
        self.border_radius = border_radius.only(top_left=self.border_radius_topLeft, top_right=self.border_radius_topRight, bottom_left=self.border_radius_bottomLeft, bottom_right=self.border_radius_bottomRight)

    def set_border_width(self, value):
        value = int(value)
        self.set_border(value)

    def set_border(self, value):
        value = int(value)
        self.border_left = value
        self.border_top = value
        self.border_right = value
        self.border_bottom = value
        self.updateBorder()

    def set_border_radius(self, value):
        value = int(value)
        self.border_radius_topLeft = value
        self.border_radius_topRight = value
        self.border_radius_bottomLeft = value
        self.border_radius_bottomRight = value
        self.updateBorderRadius()

    def set_border_radius_topLeft(self, value):
        value = int(value)
        self.border_radius_topLeft = value
        self.updateBorderRadius()

    def set_border_radius_topRight(self, value):
        value = int(value)
        self.border_radius_topRight = value
        self.updateBorderRadius()

    def set_border_radius_bottomLeft(self, value):
        value = int(value)
        self.border_radius_bottomLeft = value
        self.updateBorderRadius()

    def set_border_radius_bottomRight(self, value):
        value = int(value)
        self.border_radius_bottomRight = value
        self.updateBorderRadius()

    def set_border_color(self, value):
        value = str(value)
        self.border_color = value
        self.border_left_color = value
        self.border_top_color = value
        self.border_right_color = value
        self.border_bottom_color = value
        self.updateBorder()

    def set_border_left(self, value):
        value = int(value)
        self.border_left = value
        self.updateBorder()

    def set_border_left_color(self, value):
        self.border_left_color = value
        self.updateBorder()

    def set_border_top(self, value):
        value = int(value)
        self.border_top = value
        self.updateBorder()

    def set_border_top_color(self, value):
        value = str(value)
        self.border_top_color = value
        self.updateBorder()

    def set_border_right(self, value):
        value = int(value)
        self.border_right = value
        self.updateBorder()

    def set_border_right_color(self, value):
        value = str(value)
        self.border_right_color = value
        self.updateBorder()

    def set_border_bottom(self, value):
        value = int(value)
        self.border_bottom = value
        self.updateBorder()

    def set_border_bottom_color(self, value):
        value = str(value)
        self.border_bottom_color = value
        self.updateBorder()

class EvueContainer(BaseContainer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # content
    @property
    def content(self) -> Optional[Control]:
        return self._Container__content

    @content.setter
    def content(self, value: Optional[Control]):
        
        def on_secondary_tap(e):
            pass

        self._Container__content = GestureDetector(
            content=value,
            drag_interval= 25,
            # on_tap=lambda e: print("TAP"),
            # on_tap_down=lambda e: print(
            #     f"TAP DOWN - gx: {e.global_x}, gy: {e.global_y}, lx: {e.local_x}, ly: {e.local_y}, kind: {e.kind}, {e.control}"
            # ),
            # on_tap_up=lambda e: print(
            #     f"TAP UP - gx: {e.global_x}, gy: {e.global_y}, lx: {e.local_x}, ly: {e.local_y}, kind: {e.kind}"
            # ),
            on_secondary_tap=on_secondary_tap,
            # on_secondary_tap_down=lambda e: print(
            #     f"SECONDARY TAP DOWN - gx: {e.global_x}, gy: {e.global_y}, lx: {e.local_x}, ly: {e.local_y}, kind: {e.kind}"
            # ),
            # on_secondary_tap_up=lambda e: print(
            #     f"SECONDARY TAP UP - gx: {e.global_x}, gy: {e.global_y}, lx: {e.local_x}, ly: {e.local_y}, kind: {e.kind}"
            # ),
            # on_long_press_start=lambda e: print(
            #     f"LONG PRESS START - gx: {e.global_x}, gy: {e.global_y}, lx: {e.local_x}, ly: {e.local_y}"
            # ),
            # on_long_press_end=lambda e: print(
            #     f"LONG PRESS END - gx: {e.global_x}, gy: {e.global_y}, lx: {e.local_x}, ly: {e.local_y}, vx: {e.velocity_x}, vy: {e.velocity_y}"
            # ),
            # on_secondary_long_press_start=lambda e: print(
            #     f"SECONDARY LONG PRESS START - gx: {e.global_x}, gy: {e.global_y}, lx: {e.local_x}, ly: {e.local_y}"
            # ),
            # on_secondary_long_press_end=lambda e: print(
            #     f"SECONDARY LONG PRESS END - gx: {e.global_x}, gy: {e.global_y}, lx: {e.local_x}, ly: {e.local_y}, vx: {e.velocity_x}, vy: {e.velocity_y}"
            # ),
            # on_double_tap=lambda e: print("DOUBLE TAP"),
            # on_double_tap_down=lambda e: print(
            #     f"DOUBLE TAP DOWN - gx: {e.global_x}, gy: {e.global_y}, lx: {e.local_x}, ly: {e.local_y}, kind: {e.kind}"
            # ),
            # on_enter=lambda e: print(
            #     f"ENTER - gx: {e.global_x}, gy: {e.global_y}, lx: {e.local_x}, ly: {e.local_y}, kind: {e.kind}"
            # ),
            # on_exit=lambda e: print(
            #     f"EXIT - gx: {e.global_x}, gy: {e.global_y}, lx: {e.local_x}, ly: {e.local_y}, kind: {e.kind}"
            # ),
        )
