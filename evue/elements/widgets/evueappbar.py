# -*- coding: utf-8 -*-
from loguru import logger
from math import pi
from typing import Optional
from flet import Page, Image, Container, WindowDragArea, Stack, colors, border, margin, padding, border_radius,  DragUpdateEvent, AppBar
from ..iconbutton import IconButtonElement
from .basecontainer import EvueContainer

minimized_svg = '''<?xml version="1.0" ?><svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><defs><style>.cls-1{fill:none;stroke:#000;stroke-linecap:round;stroke-linejoin:round;stroke-width:2px;}</style></defs><title/><g id="minus"><line class="cls-1" x1="7" x2="25" y1="16" y2="16"/></g></svg>
'''

class EvueAppBar(AppBar):
    def __init__(self, page:Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.page.window_title_bar_hidden = True
        self.page.window_title_bar_buttons_hidden = True
        self.sessionID = page.session_id
        self.leading_width = 0
        self.bgcolor = "transparent"
        if "height" in kwargs:
            self.height = kwargs['height']
        else:
            self.height = 40

        self._stack = Stack([])
        self._controls_ = self._stack.controls
        self.title = WindowDragArea(Container(self._stack, expand=True, padding=0, height=self.height, bgcolor="transparent"))
        
        self.iconbutton = IconButtonElement({"type": "iconbutton"}, parent=None)
        self.iconbutton.icon = "icons.CLOSE"
        self.iconbuttonContainer = EvueContainer(self.iconbutton.obj)
        self.actions = [self.iconbuttonContainer]

        self.iconbuttonContainer.content.on_enter = self.onCloseButtonEnter
        self.iconbuttonContainer.content.on_exit = self.onCloseButtonExit
        self.iconbutton.onclick = self.onCloseButtonClick

    def onCloseButtonEnter(self, element):
        self.iconbutton.background_color = "red"
        self.iconbutton.update()

    def onCloseButtonExit(self, el):
        self.iconbutton.background_color = "transparent"
        self.iconbutton.update()

    def onCloseButtonClick(self, el):
        self.page.window_close()

    @property
    def height(self):
        return self.toolbar_height
    
    @height.setter
    def height(self, value):
        self.toolbar_height = value

    def mount(self, uri):
        from evue import require
        module = require(uri)
        component = module.createComponent(sessionID=self.sessionID)
        obj = component.rootElement.obj
        self._controls_.append(obj)
        obj.bgcolor = self.bgcolor

