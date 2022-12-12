# -*- coding: utf-8 -*-
import os
import flet
from flet import Page
from flet.flet import *
from flet.flet import _connect_internal
from flet.flet import _open_flet_view
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
        permissions=None,
        view: AppViewer = FLET_APP,
        assets_dir=None,
        upload_dir=None,
        web_renderer="canvaskit",
        route_url_strategy="hash",
        **kwargs
    ):
        if target is None:
            raise Exception("target argument is not specified")

        conn = _connect_internal(
            page_name=name,
            host=host,
            port=port,
            is_app=True,
            permissions=permissions,
            session_handler=target,
            assets_dir=assets_dir,
            upload_dir=upload_dir,
            web_renderer=web_renderer,
            route_url_strategy=route_url_strategy,
        )

        url_prefix = os.getenv("FLET_DISPLAY_URL_PREFIX")
        if url_prefix is not None:
            print(url_prefix, conn.page_url)
        else:
            logger.info(f"App URL: {conn.page_url}")

        logger.info("Connected to Flet app and handling user sessions...")

        fvp = None

        if (
            (view == FLET_APP or view == FLET_APP_HIDDEN)
            and not is_linux_server()
            and url_prefix is None
        ):
            fvp = _open_flet_view(conn.page_url, view == FLET_APP_HIDDEN)
            self.pflet = fvp
            self.connetion = conn
            try:
                fvp.wait()
            except (Exception) as e:
                pass
        else:
            if view == WEB_BROWSER and url_prefix is None:
                open_in_browser(conn.page_url)
            
            terminate = threading.Event()

            def exit_gracefully(signum, frame):
                logger.info("Gracefully terminating Flet app...")
                terminate.set()

            signal.signal(signal.SIGINT, exit_gracefully)
            signal.signal(signal.SIGTERM, exit_gracefully)
            
            try:
                while True:
                    if terminate.wait(1):
                        break
            except KeyboardInterrupt:
                pass

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
    if os.path.exists(path) and path.endswith(".json"):
        with open(path, "r", encoding="utf-8") as f:
            kwargs.update(json.load(f))

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

    loaded = False
    if "view" in kwargs:
        if kwargs["view"] == "desktop":
            loaded = True
            kwargs['view'] = flet.FLET_APP
        elif kwargs["view"] == "web":
            loaded = True
            kwargs['view']= flet.WEB_BROWSER
            if 'web_renderer' in kwargs:
                if kwargs['web_renderer'] == "canvas":
                    kwargs['web_renderer'] = 'canvaskit'
                else:
                    kwargs['web_renderer'] = 'html'
            else:
                kwargs['web_renderer'] = 'canvaskit'

            globalThis.web_renderer = kwargs['web_renderer']

            t = Thread(target=startFileServer, args=(globalThis.port, globalThis.assets_dir))
            t.daemon = True
            t.start()

    projectDir = kwargs["dir"]
    if os.path.exists(projectDir):
        loaded = True
        t = Thread(target=startFileServer, args=(globalThis.port, globalThis.assets_dir))
        t.daemon = True
        t.start()
        apppy = "%s/app.py" % (projectDir)
        loadApp(apppy)

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
