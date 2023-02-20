# -*- coding: utf-8 -*-
import builtins
from flet import Page
from loguru import logger
from .router import Router
from .globalthis import globalThis
from .databinding import DataBinding
from .sessionobject import SessionObject

from typing import (
    Any,
    Optional,
    Dict,
    Mapping,
    List,
    Tuple,
    Match,
    Callable,
    Type,
    Sequence,
)

class BaseComponent(dict, SessionObject):

    def __init__(self, sessionID=None) -> None:
        super().__init__()
        self['_data_'] = {}
        self['_rootElement_'] = None
        self.pageinfo = None
        self.sessionID = sessionID
    
    def __str__(self) -> str:
        return "<%s(%s)>" % (self.__class__.__name__, id(self))

    def getElementById(self, id):
        element = self.rootElement.getElementById(id)
        if element:
            return element
        page = self.page
        if page:
            router:Router = page.router
            userid = "%s.%s" % (self.rootElement.uri, id)
            element =  router.getElementById(userid)
            return element
        return None

    def getElementByType(self, _type):
        els = []
        listElements = self.listElements
        if listElements:
            for el in listElements:
                if el.type == _type:
                    els.append(el)
        return els

    def getElementsByTagName(self, tag):
        return self.getElementByType(tag)

    def __hash__(self):
        return hash(self.rootElement)

    @property
    def eid(self):
        '''
            element用户管理使用的id
        '''
        return "%s_%d" % (self.node['type'], id(self))

    @property
    def data(self):
        return self['_data_']

    @data.setter
    def data(self, value):
        self['_data_'] = DataBinding(value, self)

    @property
    def rootElement(self):
        return self['_rootElement_']

    @rootElement.setter
    def rootElement(self, value):
        self['_rootElement_'] = value

    def __getattr__(self, name: str) -> Any:
        if name in self['_data_']:
            return self['_data_'][name]
        else:
            return getattr(self['_rootElement_'], name)

    def __setattr__(self, name: str, value: Any) -> None:
        if "_data_" in self and name in self["_data_"]:
            setattr(self['_data_'], name, value)
        else:
            super().__setattr__(name, value)
            if self.rootElement:
                setattr(self.rootElement, name, value)

    def set_binding_value(self, element, attr, key):
        if "_data_" in self:
            self['_data_'].set_binding_value(element, attr, key)
    
    @property
    def json(self):
        attributes = self.rootElement.attributes
        attributes['id'] = self.eid
        return {
            "type": self.node['type'],
            "attributes": attributes,
            "nodes": [],
            "bindings": self.bindings,
            "events": self.events,
        }

    @classmethod
    def defaut_json(cls, name, left=0, top=0):
        from .router import require
        module = require(name)
        json =  module.UserElement.defaut_json(left, top)
        return json

    def renderRoot(self):
        pass

    def onInit(self):
        pass

    def onReady(self):
        pass

    def onShow(self):
        pass

    def onHide(self):
        pass

    def onQuit(self):
        pass

    def render(self):
        pass

builtins.BaseComponent = BaseComponent
