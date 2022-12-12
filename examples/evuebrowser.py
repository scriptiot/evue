# -*- coding: utf-8 -*-
import os
import sys
import time
from loguru import logger
from evue import startApp, globalThis, EvueAppBar, Page

def on_keyboard_event(e):
    page = e.page
    if e.key == "F5":
        page.router.debugToggle()
    elif e.key == "F11":
        page.show_semantics_debugger = not page.show_semantics_debugger
        page.update()

def onAppInit(config):
    page: Page = config['page']
    page.on_keyboard_event = on_keyboard_event

if __name__ == '__main__':
    globalThis.onAppInit = onAppInit
    if len(sys.argv) == 1:
        startApp("./start.json")
    else:
        startApp(sys.argv[1])

