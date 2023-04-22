# -*- coding: utf-8 -*-
import os
import json
import flet
from flet import Page
from flet.flet import *
from flet.flet import app
from flet.flet import open_flet_view
from .globalthis import globalThis, loadApp, loadProject
from .fileserver import *
import threading
import signal
from threading import Thread
from loguru import logger
from .router import Router
from pyee import EventEmitter

os.environ["FLET_WS_MAX_MESSAGE_SIZE"] = "8000000"
def main(page: Page):
    globalThis.addSession(page)
    page.router = Router(page.session_id)
    page.event = EventEmitter()
    if hasattr(globalThis, "onCreate"):
        if globalThis.onCreate:
            if page.route == "/":
                globalThis.onCreate(page, globalThis.onAppInit)
            else:
                globalThis.firstPage.event.emit("on_route_change", page)
    else:
        logger.error("Please set right [startProject] in start.json!")

class EvueApplication(object):

    def __init__(self, closeCallback=None) -> None:
        self.closeCallback = closeCallback
        self.pflet = None
        self.connetion = None

    def startFlet(self,
        name="",
        host=None,
        port=0,
        target=None,
        auth_token=None,
        view: AppViewer = FLET_APP,
        assets_dir=None,
        upload_dir=None,
        web_renderer="canvaskit",
        route_url_strategy="hash",
        **kwargs
    ):
        app(target,
            name=name, 
            host=host, 
            port=port,
            view=view,
            assets_dir=assets_dir,
            upload_dir=upload_dir,
            web_renderer="canvaskit",
            route_url_strategy="path",
            auth_token=auth_token
        )
        self.close()

    def close(self):
        logger.info("close app!")
        if self.pflet:
            self.pflet.terminate()
            self.pflet = None
        if self.connetion:
            self.connetion.close()
            self.connetion = None

        if self.pflet is not None and not is_windows():
            try:
                logger.info(f"Flet View process {self.pflet.pid}")
                os.kill(self.pflet.pid + 1, signal.SIGKILL)
            except:
                pass
        
        if self.closeCallback:
            self.closeCallback()

def startApp(path: str, closeCallback=None, threaded=False):
    kwargs ={
        "assets_dir": "./",
        "view": "desktop",
        "web_renderer": "canvas",
        "dir": "./"
    }
    loaded = False
    if os.path.exists(path) and path.endswith("app.py"):
        app = loadApp(path)
        if app:
            if hasattr(app, "project"):
                kwargs.update(app.project)
            loaded = True

    if os.path.exists(path) and path.endswith(".json"):
        with open(path, "r", encoding="utf-8") as f:
            kwargs.update(json.load(f))
        projectDir = kwargs["dir"]
        if loaded == False:
            apppy = "%s/app.py" % (projectDir)
            if os.path.exists(apppy):
                app = loadApp(apppy)
                if app:
                    loaded = True

    if globalThis.project:
        loaded = True

    globalThis.rootcwd = os.getcwd()
    if 'assets_dir' in kwargs:
        assets_dir = os.path.normpath(os.path.abspath(kwargs['assets_dir']))
    else:
        assets_dir = globalThis.rootcwd
    kwargs['assets_dir'] = assets_dir
    globalThis.assets_dir = assets_dir

    if 'host' in kwargs and kwargs['host'] and kwargs['host'] != "0.0.0.0":
        host = kwargs['host']
    else:
        host = get_host_ip()
        kwargs['host'] = host
    globalThis.server_ip = host if host not in [None, "", "*"] else "127.0.0.1"

    if 'port' in kwargs and kwargs['port']:
        port = kwargs['port']
        globalThis.port = port
    else:
        port = get_free_tcp_port()
        globalThis.port = port
        kwargs['port'] = port


    if "view" in kwargs:
        if kwargs["view"] == "desktop":
            kwargs['view'] = flet.FLET_APP
        elif kwargs["view"] == "web":
            kwargs['view']= flet.WEB_BROWSER
            if 'web_renderer' in kwargs:
                if kwargs['web_renderer'] == "canvas":
                    kwargs['web_renderer'] = 'canvaskit'
                else:
                    kwargs['web_renderer'] = 'html'
            else:
                kwargs['web_renderer'] = 'canvaskit'

            globalThis.web_renderer = kwargs['web_renderer']

    projectDir = kwargs["dir"]
    if os.path.exists(projectDir):
        t = Thread(target=startFileServer, args=(globalThis.port, globalThis.assets_dir))
        t.daemon = True
        t.start()

    if loaded:
        sapp = EvueApplication(closeCallback)
        globalThis.evueApp = sapp
        kwargs['target'] = main
        logger.info(kwargs)
        if threaded:
            t = Thread(target=sapp.startFlet, kwargs=kwargs)
            t.daemon = True
            t.start()
        else:
            sapp.startFlet(**kwargs)
    else:
        logger.error("app loaded failed")
