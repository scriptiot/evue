# -*- coding: utf-8 -*-
from flet import Page
from .globalthis import globalThis
from .util import open_in_browser
from typing import Any
from loguru import logger
from pyee import EventEmitter


class SessionObject(object):

    def __init__(self, sessionID) -> None:
        self.sessionID = sessionID

    def getPage(self, sessionID)->Page:
        return globalThis.getPage(sessionID)

    @property
    def page(self)->Page:
        return globalThis.getPage(self.sessionID)

    @property
    def router(self):
        if self.page:
            return self.page.router
    
    @property
    def event(self) -> EventEmitter:
        if self.page:
            return self.page.event

    @property
    def isLogin(self):
        return self.page.isLogin

    def on(self, event, handler):
        self.event.on(event, handler)

    def emit(self,event: str,*args: Any,**kwargs: Any) -> bool:
        return self.event.emit(event, *args, **kwargs)

    @property
    def localstroage(self):
        return self.page.client_storage

    def getElementById(self, id):
        return self.router.getElementById(id)

    def add(self, uri, id, element):
        return self.router.add(uri, id, element)

    def update(self):
        try:
            self.page.update()
        except:
            pass

    def clipboard(self):
        globalThis.clipboard(self.sessionID)
    
    def get_clipboard_data(self):
        return globalThis.get_clipboard_data()

    def openDialog(self, uri, dirPath=None, on_accept=None, on_cancle=None, on_dismiss=None):
        return globalThis.openDialog(self.sessionID, uri, dirPath=dirPath, on_accept=on_accept, on_cancle=on_cancle, on_dismiss=on_dismiss)

    def getFileDialog(self):
        return globalThis.getFileDialog(self.sessionID)

    def getOpenFileName(self, callback, dialog_title="打开文件", initial_directory="", allowed_extensions=[], file_type="any", allow_multiple=False):
        return globalThis.getOpenFileName(self.sessionID, callback, dialog_title=dialog_title, initial_directory=initial_directory, allowed_extensions=allowed_extensions, file_type=file_type, allow_multiple=allow_multiple)

    def getOpenFileNames(self, sessionID,  callback, dialog_title="打开多个文件", initial_directory="", allowed_extensions=[], file_type="any", allow_multiple=True):
        return globalThis.getOpenFileNames(self.sessionID, callback, dialog_title=dialog_title, initial_directory=initial_directory, allowed_extensions=allowed_extensions, file_type=file_type, allow_multiple=allow_multiple)

    def getSaveFileName(self, callback, dialog_title="保存文件", file_name="", initial_directory="", file_type="any", allowed_extensions=[]):
        return globalThis.getSaveFileName(self.sessionID, callback, dialog_title=dialog_title, file_name=file_name, initial_directory=initial_directory, file_type=file_type, allowed_extensions=allowed_extensions)

    def getExistingDirectory(self, callback, dialog_title="", initial_directory=""):
        return globalThis.getExistingDirectory(self.sessionID, callback, dialog_title=dialog_title, initial_directory=initial_directory)

    def showMessage(self, msg):
        return globalThis.showMessage(self.sessionID, msg)

    def updateTitle(self, name):
        return globalThis.updateTitle(self.sessionID, name)

    def resetTitle(self):
        return globalThis.resetTitle(self.sessionID)
    
    def isPopupVisible(self):
        return globalThis.isMenuVisible(self.sessionID)

    def isMenuVisible(self):
        return globalThis.isMenuVisible(self.sessionID)

    def showMenu(self, uri, dirpath=None, x=0, y=0):
        return self.showPopup(uri, dirpath=dirpath, x=x, y=y)

    def hideMenu(self):
        return self.hidePopup()

    def showPopup(self, uri, dirpath=None, x=0, y=0, isUpdate=True):
        return globalThis.showPopup(self.sessionID, uri, dirpath=dirpath, x=x, y=y, isUpdate=isUpdate)

    def hidePopup(self):
        return globalThis.hidePopup(self.sessionID)
    
    def launch_url(self, url):
        self.page.launch_url(url)
    
    def window_destory(self):
        self.page.window_destroy()
        self.page.update()

    def window_close(self):
        self.page.window_close()
        self.page.update()

    def window_minimized(self):
        self.page.window_minimized = True
        self.page.update()

    def window_maximized(self):
        self.page.window_maximized = True
        self.page.update()
