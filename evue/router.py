# -*- coding: utf-8 -*-
import builtins
from collections import OrderedDict
from flet import Container, Stack, Page
from .globalthis import globalThis, require
from loguru import logger
from .componentmanager import componentManager
from .sessionobject import SessionObject


class Router(SessionObject):

    borders = {}

    def __init__(self, sessionID=None) -> None:
        logger.warning(sessionID)
        super().__init__(sessionID)
        self.elements = OrderedDict()
        self.paths = ["./"]
        self.pageviews = {}
        self._currentPageUri = None
        self._debug_ = False

    def add(self, uri, id, element):
        userid = "%s.%s" % (uri, id)
        element.userid = userid
        self.elements[userid] = element

    def getElementById(self, id):
        if id in self.elements:
            return self.elements[id]
        return None

    @property
    def debug(self):
        return self._debug_

    @property
    def currentPageUri(self):
        return self._currentPageUri

    @currentPageUri.setter
    def currentPageUri(self, value):
        if self._currentPageUri != value:
            self._currentPageUri = value
            self.page.event.emit("page.router.currentPageChanged", value)

    @property
    def currentPage(self):
        if self.currentPageUri in self.pageviews:
            return self.pageviews[self.currentPageUri]
        return None

    @property
    def currentPageComponent(self):
        if self.currentPageUri in self.pageviews:
            return self.pageviews[self.currentPageUri].component
        return None

    @classmethod
    def registerComponents(cls, components):
        for c in components:
            cls.registerComponent(c)

    @classmethod
    def registerComponent(cls, componentInfo):
        componentManager.registerComponent(componentInfo)

    def addPaths(self, paths):
        self.paths.extend(paths)

    def render(self, pageview):
        self.page.add(pageview)
        self.page.update()

    def createPage(self, component):
        con = Container(content=Stack([component.rootElement.obj]), expand=True)
        con.component = component
        return con

    def hideAllPages(self):
        for uri in self.pageviews:
            page = self.pageviews[uri]
            page.visible = False
    
    def mount(self, uri, parent):
        component = self.create({'path': uri}, parent)
        self.update()
        return component

    def create(self, obj, parent=None):
        uri = obj['path']
        dirPath = None
        if 'dir' in obj:
            dirPath = obj['dir']
        module = require(uri, dirPath)
        component = module.createComponent(parent=parent, pageinfo=obj, sessionID=self.page.session_id)
        if component:
            component.pageinfo = obj
        return component

    def newEvuePage(self, obj):
        uri = obj['path']
        component = self.create(obj)
        if component:
            pageview = self.createPage(component)
            self.pageviews[uri] = pageview
            self.render(pageview)
            self.currentPageUri = uri
            logger.warning("%s.onCreateFinished" % uri)
            self.page.event.emit("%s.onCreateFinished" % uri)

    def push(self, obj):
        uri = obj['path']
        if uri in self.pageviews:
            self.currentPage.visible = False
            self.currentPage.component.onHide()
            for _uri in self.pageviews:
                page = self.pageviews[_uri]
                if page:
                    if _uri != uri:
                        page.visible = False
                    else:
                        page.visible = True
                        page.component.pageinfo = obj
                        page.component.onShow()
                        self.currentPageUri = uri
            globalThis.update()
        else:
            self.hideAllPages()
            self.newEvuePage(obj)

    def replace(self, obj):
        if self.currentPage in globalThis.page.controls:
            globalThis.page.controls.remove(self.currentPage)
            self.pageviews.pop(self.currentPageUri)
            self._currentPageUri = None
            globalThis.update()

        self.hideAllPages()
        self.newEvuePage(obj)

    def debugToggle(self):
        from .elements import ElementInstances
        self._debug_ = not self._debug_

        def debugPageViewOn():
            for eid in ElementInstances:
                element = ElementInstances[eid]
                if eid not in self.borders:
                    self.borders[eid] = {
                        "border_width" : element.border_width,
                        "border_radius" : element.border_radius,
                        "border_color" : element.border_color
                    }
                element.debug_on()

        def debugPageViewOff():
            for eid in ElementInstances:
                element = ElementInstances[eid]
                element.debug_off()
                border = self.borders[eid]
                element.border_width = border['border_width']
                element.border_radius = border['border_radius']
                element.border_color = border['border_color']

        if self._debug_:
            debugPageViewOn()
        else:
            debugPageViewOff()

builtins.Router = Router
