# -*- coding: utf-8 -*-
from .fletbaseelement import FletBaseElement
from flet import (
    Stack,
    Text,
    AlertDialog,
    TextButton
)
from flet_core.buttons import *
from ..globalthis import globalThis
from .widgets import BaseContainer


class DialogElement(FletBaseElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self.create(parent, draggable)
        self.setParent(parent)

    def create(self, parent, draggable=False):
        self._stack_ = Stack([])
        self._obj_ = BaseContainer(
            self._stack_,
        )
        self._controls_ = self._stack_.controls
        self._dialog_ = AlertDialog(content=self._obj_, shape=RoundedRectangleBorder(radius=10))
        self._dialog_.parentElement = self

        def close_dlg(e):
            self._dialog_.open = False
            self.page.update()

        actions=[
            TextButton("确定", on_click=close_dlg),
            TextButton("取消", on_click=close_dlg),
        ]
        self._dialog_.actions = actions

    @property
    def isContainer(self):
        return True

    def set_open(self, value):
        self._dialog_.open = self.bool(value)

    def set_title(self, value):
        self._dialog_.title = Text(value)

    def set_modal(self, value):
        self._dialog_.modal = self.bool(value)

    def set_title_padding(self, value):
        self._dialog_.title_padding = value

    def set_content_padding(self, value):
        self._dialog_.content_padding = value
    
    def set_actions_alignment(self, value):
        self._dialog_.actions_alignment = value
    
    def set_actions_texts(self, value):
        if self._dialog_.actions:
            textButton0:TextButton = self._dialog_.actions[0]
            textButton0.text = value[0]
            textButton1:TextButton = self._dialog_.actions[1]
            textButton1.text = value[1]

    def set_action_enter_text(self, value):
        if self._dialog_.actions:
            textButton:TextButton = self._dialog_.actions[0]
            textButton.text = value
    
    def set_action_cancel_text(self, value):
        if self._dialog_.actions:
            textButton:TextButton = self._dialog_.actions[1]
            textButton.text = value
            

    def set_onAccept(self, func):
        def action(e):
            self._dialog_.open = not func(e)
            self.page.update()
            if not self._dialog_.open:
                self.page.dialog  = None

        self._dialog_.actions[0].on_click = action

    def set_onCancel(self, func):
        def action(e):
            self._dialog_.open = not func(e)
            self.page.update()
            if not self._dialog_.open:
                self.page.dialog  = None
        self._dialog_.actions[1].on_click = action

    def set_onDismiss(self, func):
        def action(e):
            self._dialog_.open = not func(e)
            self.page.update()
            if not self._dialog_.open:
                self.page.dialog  = None
        self._dialog_.on_dismiss = action

    def set_border_radius(self, value):
        self._dialog_.shape = RoundedRectangleBorder(radius=value)

    @property
    def attributes(self):
        attributes = super().attributes
        attributes.update({
            "open": self._dialog_.open,
            "title": self._dialog_.title,
            "modal": self._dialog_.modal,
            "title_padding": self._dialog_.title_padding,
            "content_padding": self._dialog_.content_padding,
            "border-radius": 10
        })
        return attributes
