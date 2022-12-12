# -*- coding: utf-8 -*-
import os, sys
import json
import builtins
from importlib import util
from flet import Page, utils, SnackBar, Text, FilePicker
from pyee import EventEmitter
from typing import Any
from loguru import logger
import pyperclip
import subprocess
from threading import Thread
import functools
from collections import OrderedDict


_modules_ = {}

def threaded(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        t = Thread(target=fn, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return wrapper

def load_module(path):
    spec = util.spec_from_file_location('', path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def loadApp(path):
    if os.path.exists(path):
        d = os.path.dirname(path)
        sys.path.insert(0, d)
        load_module(path)
        return True
    return False

def loadProject(path):
    if os.path.exists(path):
        d = os.path.dirname(path)
        sys.path.insert(0, d)
        with open(path, "r", encoding="utf-8") as f:
            project = json.loads(f.read())
        return project
    return None

def _require_(path, force=False):
    if path in _modules_ and force == False:
        return _modules_[path]
    module = load_module(path)
    module.__name__ = "[%s.evue]UserComponent" % os.path.basename(path)[0:-3]
    _modules_[path] = module
    return module

def require(uri, dirPath=None, force=False):
    if uri in _modules_ and force == False:
        return _modules_[uri]

    if os.path.exists(uri):
        path = uri
    else:
        if not uri.endswith(".py"):
            uri = "%s.py" % uri
        if dirPath is None:
            path = os.path.normpath("%s" % uri)
        else:
            path = os.path.normpath("%s/%s" % (dirPath, uri))
    return _require_(path, force)

class globalThis(object):
    rootcwd = os.getcwd()
    server_ip = '127.0.0.1'
    port = None
    sessions = OrderedDict()

    startProjectDir = None
    project = None
    app = None
    firstPage:Page = None
    page:Page = None
    event = EventEmitter()
    assets_dir = None
    web_renderer = None
    webprocess = None
    
    evueApp = None
    onAppInit = None

    @classmethod
    def isWeb(cls):
        return cls.web_renderer is not None

    @classmethod
    def rootDesignerDir(cls):
        return "%s/designer" % (cls.rootcwd)

    @classmethod
    def addSession(cls, page: Page):
        cls.page = page
        cls.sessions[page.session_id] = page
        page.on_connect = cls.on_connect
        page.on_disconnect = cls.on_disconnect

    @classmethod
    def on_connect(cls, event):
        session_id = event.page.session_id
        globalThis.sessions[session_id] = event.page

    @classmethod
    def on_disconnect(cls, event):
        from evue.router import Router
        session_id = event.page.session_id
        if session_id in globalThis.sessions:
            page:Page = globalThis.sessions[session_id]
            router: Router = page.router
            for uri, pageview in router.pageviews.items():
                component = pageview.component
                if hasattr(component, "onQuit"):
                    component.onQuit()
            if page == globalThis.firstPage:
                if globalThis.onDestroy:
                    globalThis.onDestroy()
                globalThis.firstPage = None
            del globalThis.sessions[session_id]

    @classmethod
    def getPage(cls, sessionID):
        if sessionID in globalThis.sessions:
            return globalThis.sessions[sessionID]
        return None

    @classmethod
    def pages(cls):
        return list(globalThis.sessions.values())

    @classmethod
    def update(cls):
        if isinstance(cls.page, Page):
            cls.page.update()

    @classmethod
    def on(cls, event, handler):
        cls.event.on(event, handler)

    @classmethod
    def emit(cls,event: str,*args: Any,**kwargs: Any) -> bool:
        return cls.event.emit(event, *args, **kwargs)

    @classmethod
    def set_clipboard_data(self, text):
        pyperclip.copy(text)

    @classmethod
    def get_clipboard_data(cls):
        if utils.is_windows():
            from win32 import win32clipboard as w
            CF_TEXT = 1
            CF_HDROP = 15
            w.OpenClipboard()
            try:
                d = w.GetClipboardData(CF_TEXT)
                w.CloseClipboard()
                return d.decode('GBK')
            except:
                try:
                    d = w.GetClipboardData(CF_HDROP)
                    w.CloseClipboard()
                except:
                    d = pyperclip.paste()
                return d
        else:
            return pyperclip.paste()

    @classmethod
    def clipboard(cls, sessionID):
        page = cls.getPage(sessionID)
        clipboard = page._Page__offstage.clipboard
        logger.warning(clipboard.value)

    @classmethod
    def openDialog(cls, sessionID, uri, dirPath=None, on_accept=None, on_cancle=None, on_dismiss=None):
        page = cls.getPage(sessionID)
        logger.warning(page.dialog)
        if page.dialog:
            page.dialog = None
            page.update()
        if page.dialog is None:
            module = require(uri, dirPath)
            pageview = module.createComponent(sessionID=sessionID)
            dialog = pageview.rootElement 
            
            def onAccept(e):
                logger.warning(e)
                ret = True
                if hasattr(pageview, "onAccept") and pageview.onAccept:
                    ret = pageview.onAccept(dialog)
                if on_accept:
                    ret = on_accept(dialog.id, pageview, True)
                logger.warning(ret)
                if ret:
                    page.event.emit(dialog.id, pageview, True)
                return ret

            def onCancel(e):
                ret = True
                if hasattr(pageview, "onCancel") and pageview.onCancel:
                    ret = pageview.onCancel(dialog)
                
                logger.warning(on_cancle)
                if on_cancle:
                    ret = on_cancle(dialog.id, pageview, False)
                if ret:
                    page.event.emit(dialog.id, pageview, False)
                    # page.dialog = None
                
                logger.warning(ret)
                return ret

            def onDismiss(e):
                ret = True
                if hasattr(pageview, "onDismiss") and pageview.onDismiss:
                    ret = pageview.onDismiss(dialog)
                if on_dismiss:
                    ret = on_dismiss(dialog.id, pageview, False)
                return ret

            dialog.onAccept = onAccept
            dialog.onCancel = onCancel
            dialog.onDismiss = onDismiss
            dialog.open = True
            page.dialog = dialog._dialog_
            page.update()
            return pageview
        else:
            return None

    @classmethod
    def getFileDialog(cls, sessionID):
        page = cls.getPage(sessionID)
        pick_files_dialog = page.overlay[0]
        pick_files_dialog.on_result._EventHandler__handlers.clear()
        return pick_files_dialog

    @classmethod
    def getOpenFileName(cls, sessionID, callback, dialog_title="打开文件", initial_directory="", allowed_extensions=[], file_type="any", allow_multiple=False):
        pick_files_dialog = cls.getFileDialog(sessionID)
        pick_files_dialog.on_result = callback
        pick_files_dialog.pick_files(
            dialog_title,
            initial_directory,
            file_type,
            allowed_extensions,
            allow_multiple
        )


    @classmethod
    def getOpenFileNames(cls, sessionID,  callback, dialog_title="打开多个文件", initial_directory="", allowed_extensions=[], file_type="any", allow_multiple=True):
        pick_files_dialog = cls.getFileDialog(sessionID)
        pick_files_dialog.on_result = callback
        pick_files_dialog.pick_files(
            dialog_title,
            initial_directory,
            file_type,
            allowed_extensions,
            allow_multiple
        )

    @classmethod
    def getSaveFileName(cls, sessionID, callback, dialog_title="保存文件", file_name="", initial_directory="", file_type="any", allowed_extensions=[]):
        pick_files_dialog = cls.getFileDialog(sessionID)
        pick_files_dialog.on_result = callback
        pick_files_dialog.save_file(
            dialog_title,
            file_name,
            initial_directory,
            file_type,
            allowed_extensions
        )

    @classmethod
    def getExistingDirectory(cls, sessionID, callback, dialog_title="", initial_directory=""):
        pick_files_dialog = cls.getFileDialog(sessionID)
        pick_files_dialog.on_result = callback
        pick_files_dialog.get_directory_path(
            dialog_title,
            initial_directory
        )
    
    @classmethod
    def showMessage(cls, sessionID,  msg):
        page = cls.getPage(sessionID)
        snack_bar = SnackBar(Text(f"%s" % msg))
        page.snack_bar = snack_bar
        page.snack_bar.open = True
        page.update()

    @classmethod
    def updateTitle(cls, sessionID, name):
        page = cls.getPage(sessionID)
        page.title = "Evue Designer [%s]" % name
        page.update()
    
    @classmethod
    def resetTitle(cls, sessionID):
        page = cls.getPage(sessionID)
        page.title = "Evue Designer"
        page.update()
    
    @classmethod
    def isMenuVisible(cls, sessionID):
        page = cls.getPage(sessionID)
        return page.splash is not None

    @classmethod
    def showMenu(cls, sessionID, uri, dirpath=None, x=0, y=0):
        return cls.showPopup(sessionID, uri, dirpath, x, y)
    
    @classmethod
    def hideMenu(cls, sessionID):
        cls.hidePopup(sessionID)

    @classmethod
    def showPopup(cls, sessionID, uri, dirpath=None, x=0, y=0, isUpdate=True):
        page = cls.getPage(sessionID)
        module = require(uri, dirpath)
        pageview = module.createComponent(sessionID=sessionID)
        rootElement = pageview.rootElement
        splash = rootElement.obj
        splash.left = x
        splash.top = y
        page.splash = splash
        if isUpdate:
            page.update()
        return pageview

    @classmethod
    def hidePopup(cls, sessionID):
        page = cls.getPage(sessionID)
        page.splash = None
        page.update()

    @classmethod
    def runCmd(cls, command, callback=None):
        logger.warning(command)
        ret = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8")
        @threaded
        def log():
            logger.warning(ret.communicate()[0])
            if callback:
                callback()
        log()
        return ret


def EvueApp(config):
    sys.path.extend(config["paths"])
    logger.warning(os.getcwd())
    def onCreate(page: Page, onAppInit=None):
        logger.warning(os.getcwd())
        from .router import Router

        if globalThis.firstPage is None:
            globalThis.firstPage = page

        pick_files_dialog = FilePicker()
        page.overlay.extend([pick_files_dialog])

        if globalThis.project:
            page.window_width = globalThis.project['width']
            page.window_height = globalThis.project['height'] + 60

        page.window_center()

        for key in config:
            if hasattr(page, key):
                setattr(page, key, config[key])

        _onCreate = config['onCreate']
        config['sessionID'] = page.session_id
        config['page'] = page

        if 'appDir' not in config:
            config['appDir'] = globalThis.startProjectDir
        os.chdir(config['appDir'])

        if onAppInit:
            onAppInit(config)

        _onCreate(config)

        logger.warning(config)
        page.router.replace({
            'path': config['uri']
        })

        page.event.emit("app.onCreateFinished", page)

    globalThis.onCreate = onCreate
    globalThis.onDestroy = config['onDestroy']


builtins.EvueApp = EvueApp
builtins.globalThis = globalThis

