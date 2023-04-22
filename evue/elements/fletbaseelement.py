# -*- coding: utf-8 -*-
import os
from .base import BaseElement
from flet import (
    Page,
    alignment,
    border,
    border_radius,
    DragUpdateEvent,
    GestureDetector,
    MouseCursor,
    LinearGradient,
    RadialGradient,
    SweepGradient
)
from flet_core.alignment import Alignment
from ..router import Router
from ..globalthis import globalThis, require
from ..pyrect import Rect
from pyee import EventEmitter
from typing import Any, OrderedDict
from dataclasses import dataclass
from loguru import logger
from .widgets import BaseContainer

@dataclass
class Point:
    x: int
    y: int

ElementInstances = {} #所有的elemnt实例对象, 用于内部管理

class FletBaseElement(BaseElement):

    cornor_size = 20

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(sessionID)
        self['draggable'] = draggable
        self._debug_on = False
        self.id = None
        self.node = node
        self.parent = parent
        self._obj_ = None
        self._elements_ = OrderedDict()
        self._event_ = EventEmitter()
        ElementInstances[self.eid] = self
        self.uri = None # uri 主要记录evue文件的名称uri
        self.userid = None # uri.id 主要用于evue文件中根据uri.id索引元素
        self._borders_ = {} # 记录元素的border值
        self.events = {} # 记录元素的events
        self.bindings = [] # 记录元素的bindings
        self.resources = {} # 记录元素的资源
        self['_mouseEvent_'] = None
        self['_isCreateFinished_'] = None

    def add(self, sessionID, uri, id, element):
        page = self.getPage(sessionID)
        if page:
            from ..router import Router
            router:Router = page.router
            router.add(uri, id, element)

    @property
    def isUserElement(self):
        return self.__class__.__name__ == "UserElement"

    @property
    def eid(self):
        '''
            element内部管理使用唯一id
        '''
        return "%s_%s" % (self.type, str(id(self))[-6:-1])

    @property
    def type(self):
        return self.node['type']

    def mapFromGlobal(self, x, y):
        px = x - self.left
        py = y - self.top
        return Point(px, py)

    def mapToParentRect(self, element):
        parent = self['parent']
        left = self.rect.left
        top = self.rect.top
        width = self.rect.width
        height = self.rect.height
        while True:
            if parent == element:
                return Rect(left, top, width, height)
            else:
                left += parent.rect.left
                top += parent.rect.top
                parent = parent['parent']
        return self.rect

    def mapToLocal(self, parentElement, px, py):
        point = []
        def mapPoint(point, element, lx, ly):
            for eid in element.elements:
                el = element.elements[eid]
                _x = lx - el.left
                _y = ly - el.top
                if el == self:
                    point.append(_x)
                    point.append(_y)
                    return point
                if el.isLayout:
                    continue
                mapPoint(point, el, _x, _y)
            return point
        point  = mapPoint(point, parentElement, px, py)
        return point


    def isPointIn(self, x, y):
        p = self.mapFromGlobal(x, y)
        if p.x < 0 or p.y < 0  or p.x > (self.left + self.width) or p.y > (self.top + self.height):
            return False
        return True

    def on(self, event, *args, **kwargs):
        self._event_.on(event, *args, **kwargs)

    def emit(self, event: str,*args: Any,**kwargs: Any) -> bool:
        return self._event_.emit(event, *args, **kwargs)

    def createChildComponent(self):
        childId = "%s%d" % (self.child, self.childCount)
        module = require(self.child, os.getcwd())
        pageview = module.createComponent(self, sessionID=self.sessionID)
        element = pageview.rootElement
        self.add(self.sessionID, self.id, childId, element)
        return pageview

    def set_for_data(self, items):
        if self['_isCreateFinished_']:
            self.clearChildren()
            for i, item in enumerate(items):
                pageview = self.createChildComponent()
                for key, value in item.items():
                    setattr(pageview, key, value)

    def onCreatedFinished(self):
        self['_isCreateFinished_'] = True
        if self.isContainer and 'for_data' in self and self.for_data:
            self.set_for_data(self.for_data)

    @property
    def isContainer(self):
        return False
    
    @property
    def isLayout(self):
        return False

    @property
    def hasTextProperty(self):
        defaut_style = self.defaut_style()
        return 'color' in defaut_style and \
            'font-size' in defaut_style and \
            'text-align' in defaut_style

    @property
    def controls(self):
        return self._controls_

    def childAdded(self, element):
        pass

    def setParent(self, parent):
        if parent and parent.isContainer:
            self['parent'] = parent
            self['index'] = len(parent._controls_)
            parent._controls_.append(self.obj)
            parent.elements[self.eid] = self
            parent.childAdded(self)

            # from .responsiverow import ResponsiveRowElement
            # if isinstance(parent, ResponsiveRowElement):
            #     self.col = parent['col']

    def delete_control(self):
        try:
            parent = self['parent']
            parent._controls_.remove(self.obj)
            parent.update()
        except:
            pass

    def delete(self, isRoot=True):
        els = self.elements.values()
        for child in els:
            child.delete(False)

        parent = self['parent']
        self.delete_control()

        if self.eid in ElementInstances:
            ElementInstances.pop(self.eid) # 从全局ElementInstances中移除

        if isRoot:
            parent.remove(self.eid) #从父Element的elements中移除
        self.clearChildren()
        del self

    def resetParent(self, element):
        self.delete_control()
        parent = self['parent']
        parent.remove(self.eid) #从父Element的elements中移除
        self.setParent(element)
        # element.add(self.uri, self.id, self)
    
    def clearChildren(self):
        elements = self._elements_
        keys = list(elements.keys())
        for eid in keys:
            element = elements[eid]
            element.delete()
        self.removeChildren()

    def align_element_bottom(self):
        parent = self['parent']
        obj = self.obj
        objs = parent._controls_
        objs.remove(obj)
        objs.insert(0, obj)
        self.update()

        _elements = OrderedDict()
        _elements[self.eid] = self
        _elements.update(parent._elements_)
        parent._elements_ = _elements

    def align_element_top(self):
        parent = self['parent']
        obj = self.obj
        objs = parent._controls_
        objs.remove(obj)
        objs.append(obj)
        self.update()

        parent._elements_.pop(self.eid)
        parent._elements_[self.eid] = self

    @property
    def childCount(self):
        return len(self._elements_)

    @property
    def elements(self):
        return self._elements_
    
    @property
    def listElements(self):
        return list(self._elements_.values())

    @elements.setter
    def elements(self, value):
        self._elements_ = value

    def removeChildren(self):
        if hasattr(self, "controls"):
            self.controls.clear()
        self._elements_ = {}

    def remove(self, id):
        if id in self._elements_:
            self._elements_.pop(id)

    def getElementById(self, id):
        if id == "None":
            return None
        elif id is None:
            return None
        if id == self.id:
            return self

        def getChild(parent):
            elements = parent._elements_
            for eid in elements:
                element = elements[eid]
                if element.id == id:
                    return element
                else:
                    el = getChild(element)
                    if el:
                        return el
                    else:
                        continue
            return None

        return getChild(self)

    def __str__(self) -> str:
        if "type" in self.node:
            return "<%sElement(%s)>" % (self.type.capitalize(), self.eid)
        else:
            return self.__class__.__name__

    def __repr__(self) -> str:
        return str(self)

    def __lt__(self,other):
        if self.area < other.area:
            return True
        else:
            if self.area == other.area:
                return True if self.width < other.width else False
            else:
                return False

    def __gt__(self,other):
        if self.area > other.area:
            return True
        else:
            if self.area == other.area:
                return True if self.width > other.width else False
            else:
                return False

    @property
    def obj(self)->BaseContainer:
        return self._obj_

    @property
    def rect(self):
        return Rect(self.left, self.top, self.width, self.height)

    @property
    def leftSideRectCornor(self):
        cornor_size = FletBaseElement.cornor_size
        return Rect(0, cornor_size, cornor_size, self.height - cornor_size * 2)

    @property
    def topSideRectCornor(self):
        cornor_size = FletBaseElement.cornor_size
        return Rect(cornor_size, 0, self.width - cornor_size * 2, cornor_size)

    @property
    def rightSideRectCornor(self):
        cornor_size = FletBaseElement.cornor_size
        return Rect(self.width - cornor_size, cornor_size, cornor_size, self.height - cornor_size * 2)

    @property
    def bottomSideRectCornor(self):
        cornor_size = FletBaseElement.cornor_size
        return Rect(cornor_size, self.height - cornor_size, self.width - cornor_size * 2, cornor_size)

    @property
    def topLeftRectCornor(self):
        cornor_size = FletBaseElement.cornor_size
        return Rect(0, 0, cornor_size, cornor_size)

    @property
    def topRightRectCornor(self):
        cornor_size = FletBaseElement.cornor_size
        return Rect(self.width - cornor_size, 0, cornor_size, cornor_size)

    @property
    def bottomLeftRectCornor(self):
        cornor_size = FletBaseElement.cornor_size
        return Rect(0, self.height - cornor_size, cornor_size, cornor_size)

    @property
    def bottomRightRectCornor(self):
        cornor_size = FletBaseElement.cornor_size
        return Rect(self.width - cornor_size, self.height - cornor_size, cornor_size, cornor_size)

    @property
    def area(self):
        return self.width * self.height

    @property
    def layout(self):
        return self._obj_

    def __hash__(self):
        return hash(id(self))

    def update(self):
        self.obj.update()

    def show(self):
        self.visible = True
        if hasattr(self, "component"):
            self.component.onShow()

    def hide(self):
        self.visible = False
        if hasattr(self, "component"):
            self.component.onHide()

    def set_visible(self, value):
        self.obj.visible = BaseElement.bool(value)

    def set_align_items(self, value):
        if value == "top_left":
            self._obj_.alignment = alignment.top_left
        elif value == "top_center":
            self._obj_.alignment = alignment.top_center
        elif value == "top_right":
            self._obj_.alignment = alignment.top_right
        elif value in ["center_left", "left"]:
            self._obj_.alignment = alignment.center_left
        elif value == "center":
            self._obj_.alignment = alignment.center
        elif value in ["center_right", "right"]:
            self._obj_.alignment = alignment.center_right
        elif value == "bottom_left":
            self._obj_.alignment = alignment.bottom_left
        elif value == "bottom_center":
            self._obj_.alignment = alignment.bottom_center
        elif value == "bottom_right":
            self._obj_.alignment = alignment.bottom_right

    def set_alignment(self, value):
        self.set_align_items(value)

    def set_expand(self, expand):
        self.obj.expend = BaseElement.bool(expand)
    
    def set_disabled(self, value):
        self.obj.disabled = FletBaseElement.bool(value)

    def set_tooltip(self, value):
        self.obj.tooltip = value

    def set_left(self, value):
        if self['parent'] and self['parent'].isLayout:
            return
        if value is None:
            self.obj.left = None
        else:
            self.obj.left = int(value)

    def set_top(self, value):
        if self['parent'] and self['parent'].isLayout:
            return
        if value is None:
            self.obj.top = None
        else:
            self.obj.top = int(value)

    def set_margin(self, value):
        self.obj.set_margin(value)

    def set_margin_left(self, value):
        self.obj.set_margin_left(value)

    def set_margin_top(self, value):
        self.obj.set_margin_top(value)

    def set_margin_right(self, value):
        self.obj.set_margin_right(value)

    def set_margin_bottom(self, value):
        self.obj.set_margin_bottom(value)

    def set_padding(self, value):
        self.obj.set_padding(value)

    def set_padding_left(self, value):
        self.obj.set_padding_left(value)

    def set_padding_top(self, value):
        self.obj.set_padding_top(value)

    def set_padding_right(self, value):
        self.obj.set_padding_right(value)

    def set_padding_bottom(self, value):
        self.obj.set_padding_bottom(value)

    def set_border(self, value):
        self.obj.set_border(value)

    def set_border_width(self, value):
        self.obj.set_border_width(value)

    def set_border_left(self, value):
        self.obj.set_border_left(value)
    
    def set_border_left_color(self, value):
        self.obj.set_border_left_color(value)

    def set_border_top(self, value):
        self.obj.set_border_top(value)

    def set_border_top_color(self, value):
        self.obj.set_border_top_color(value)

    def set_border_right(self, value):
        self.obj.set_border_right(value)

    def set_border_right_color(self, value):
        self.obj.set_border_right_color(value)

    def set_border_bottom(self, value):
        self.obj.set_border_bottom(value)

    def set_border_bottom_color(self, value):
        self.obj.set_border_bottom_color(value)

    def set_border_color(self, value):
        self.obj.set_border_color(value)

    def set_border_radius(self, value):
        self.obj.set_border_radius(value)

    def set_border_radius_topLeft(self, value):
        self.obj.set_border_radius_topLeft(value)

    def set_border_radius_topRight(self, value):
        self.obj.set_border_radius_topRight(value)

    def set_border_radius_bottomLeft(self, value):
        self.obj.set_border_radius_bottomLeft(value)

    def set_border_radius_bottomRight(self, value):
        self.obj.set_border_radius_bottomRight(value)

    def set_background_color(self, value):
        value = str(value)
        self.obj.bgcolor = value

    def set_background_image(self, value):
        logger.warning(value)
        if isinstance(value, str):
            if value.startswith("linear-gradient"):
                pass
            elif value.startswith("LinearGradient"):
                self.obj.gradient = eval(value)
            elif value.startswith("RadialGradient"):
                self.obj.gradient = eval(value)
            elif value.startswith("SweepGradient"):
                self.obj.gradient = eval(value)

    def set_gradient(self, value):
        self.set_background_image(value)

    def set_opacity(self, value):
        value = float(value)
        self.obj.opacity = value

    def set_rotate(self, value):
        value = float(value)
        self.obj.rotate = value

    def set_scale(self, value):
        value = float(value)
        self.obj.scale = value

    def set_offset(self, value):
        value = float(value)
        self.obj.offset = value
    
    def set_col(self, value):
        if isinstance(value, str):
            col = {}
            items = value.split("-")
            for i in range(0, int(len(items)/2)):
                col[items[i * 2]] = int(items[i * 2+1])
            self.obj.col = col
        else:
            self.obj.col = value

    @property
    def borders(self):
        return self._borders_

    def updateBorders(self):
        self._borders_ = {
                "border-width" : self.border_width,
                "border-radius" : self.border_radius,
                "border-color" : self.border_color
            }

    def restoreBorders(self):
        self.border_width = self._borders_['border-width']
        self.border_radius = self._borders_['border-radius']
        self.border_color = self._borders_['border-color']

    @property
    def isChildDebugOn(self):
        for eid in self._elements_:
            cel = self._elements_[eid]
            if cel._debug_on:
                return True
        return False

    @property
    def isDebugOn(self):
        return self._debug_on

    def debug_on(self):
        if not self._debug_on:
            self._debug_on = True
            self.updateBorders()
            if self.border_width <= 1:
                self.border_width = 1
            else:
                self.border_width += 1

            if self.border_color == "transparent":
                if self.isContainer:
                    self.border_color = 'green'
                else:
                    self.border_color = 'red'

    def debug_off(self):
        if self._debug_on:
            self._debug_on = False
            self.restoreBorders()

    @property
    def mouseEvent(self):
        return self['_mouseEvent_']

    def set_mouseEvent(self, value):
        self['_mouseEvent_'] = value

    def getElementByPoint(self, x, y):
        mouseInElements = []
        def _getElementByPoint(element, lx, ly):
            for eid in element.elements:
                el = element.elements[eid]
                try:
                    if (lx, ly) in el.rect:
                        mouseInElements.append(el)
                        _x = lx - el.left
                        _y = ly - el.top
                        _getElementByPoint(el, _x, _y)
                except:
                    pass
            return mouseInElements
        return _getElementByPoint(self, x, y)

    def set_onpress(self, value):
        if value:
            def on_tap_down(e):
                self['_mouseEvent_'] = e
                value(self)

            if isinstance(self.obj.content, GestureDetector):
                self.obj.content.on_tap_down = on_tap_down

    def set_onrelease(self, value):
        if value:
            def on_tap_up(e):
                self['_mouseEvent_'] = e
                value(self)

            if isinstance(self.obj.content, GestureDetector):
                self.obj.content.on_tap_up = on_tap_up

    def set_onclick(self, value):
        if value:
            def on_click(e):
                self['_mouseEvent_'] = e
                value(self)
            if self.node['type'] == "button" or self.node['type'] == "iconbutton":
                self._button_.on_click = on_click
            else:
                self._obj_.on_click = on_click

            # if isinstance(self.obj.content, GestureDetector):
            #     self.obj.content.on_tap = on_click

    def set_onlongpress(self, value):
        if value:
            def on_long_press(e):
                self['_mouseEvent_'] = e
                value(self)
            self.obj.on_long_press = on_long_press
            
            if isinstance(self.obj.content, GestureDetector):
                self.obj.content.on_long_press_start = on_long_press

    def set_ondoubleclick(self, value):
        if value:
            def on_double_tap_down(e):
                self['_mouseEvent_'] = e

            def on_double_tap(e):
                value(self)

            if isinstance(self.obj.content, GestureDetector):
                self.obj.content.on_double_tap_down = on_double_tap_down
                self.obj.content.on_double_tap = on_double_tap

    def set_onrightclick(self, value):
        if value:
            def on_secondary_tap_down(e):
                self['_mouseEvent_'] = e
                value(self)
            if isinstance(self.obj.content, GestureDetector):
                self.obj.content.on_secondary_tap_down = on_secondary_tap_down

    def set_onhover(self, value):
        if value:
            def on_hover(e):
                self['_mouseEvent_'] = e
                value(self)
            if isinstance(self.obj.content, GestureDetector):
                self.obj.content.on_hover = on_hover

    def set_onenter(self, value):
        if value:
            def on_enter(e):
                self['_mouseEvent_'] = e
                value(self)
            if isinstance(self.obj.content, GestureDetector):
                self.obj.content.on_enter = on_enter

    def set_onexit(self, value):
        if value:
            def on_exit(e):
                self['_mouseEvent_'] = e
                value(self)
            if isinstance(self.obj.content, GestureDetector):
                self.obj.content.on_exit = on_exit

    def set_on_pan_start(self, value):
        def on_pan_start(e: DragUpdateEvent):
            if value:
                self['_mouseEvent_'] = e
                value(self)
        if isinstance(self.obj.content, GestureDetector):
            self.obj.content.on_pan_start = on_pan_start

    def set_on_pan_update(self, value):
        def on_pan_update(e: DragUpdateEvent):
            if value:
                self['_mouseEvent_'] = e
                value(self)
        if isinstance(self.obj.content, GestureDetector):
            self.obj.content.on_pan_update = on_pan_update

    def set_on_pan_end(self, value):
        def on_pan_end(e: DragUpdateEvent):
            if value:
                self['_mouseEvent_'] = e
                value(self)
        if isinstance(self.obj.content, GestureDetector):
            self.obj.content.on_pan_end = on_pan_end

    def set_cursor(self, coursor):
        if isinstance(self.obj.content, GestureDetector):
            self.obj.content.mouse_cursor = coursor

    def set_href(self, value):
        def on_click(e):
            self['_mouseEvent_'] = e
            if click:
                click(self)
            if value:
                self.page.launch_url(value)

        click = None
        if self.node['type'] == "button" or self.node['type'] == "iconbutton":
            click = self['onclick']

        if self.node['type'] == "button":
            self._button_.on_click = on_click
        else:
            self._obj_.on_click = on_click

    def set_push(self, value):
        def on_click(e):
            self['_mouseEvent_'] = e
            if click:
                click(self)
            if value:
                self.router.push({'path': value})

        click = None
        if self.node['type'] == "button" or self.node['type'] == "iconbutton":
            click = self['onclick']

        if self.node['type'] == "button" or self.node['type'] == "iconbutton":
            self._button_.on_click = on_click
        else:
            self._obj_.on_click = on_click

    def set_replace(self, value):
        def on_click(e):
            self['_mouseEvent_'] = e
            if click:
                click(self)
            if value:
                self.router.replace({'path': value})

        click = None
        if self.node['type'] == "button" or self.node['type'] == "iconbutton":
            click = self['onclick']

        if self.node['type'] == "button":
            self._button_.on_click = on_click
        else:
            self._obj_.on_click = on_click

    @property
    def attributes(self):
        if self.id:
            _id = self.id
        else:
            _id = self.eid
        return {
            'id': _id,
            'style': self.style
        }

    @property
    def style(self):
        ret = {
            "left": self.left,
            "top": self.top,
            "border-width": self.border_width,
            "border-color": self.border_color,
            "border-radius": self.border_radius,
            "background-color": self.background_color,
            "padding-left": self.padding_left,
            "padding-top": self.padding_top,
            "padding-right": self.padding_right,
            "padding-bottom": self.padding_bottom
        }
        if int(self.width) > 0:
            ret['width'] = int(self.width)
        if int(self.height) > 0:
            ret['height'] = int(self.height)

        if int(self.width) == 0 and int(self.height) == 0:
            ret['right'] = 0
            ret['bottom'] = 0

        ret.update(self._borders_)
        return ret

    @property
    def json(self):
        for b in self.bindings:
            b['value'] = getattr(self, b['attrName'])
        return {
            "type": self.node['type'],
            "attributes": self.attributes,
            "nodes": [],
            "bindings": self.bindings,
            "events": self.events,
        }

    def set_attributes(self, node):
        attributes = node['attributes']
        # css
        style = attributes['style']
        if 'left' in style:
            self.left = style['left']
        if 'top' in style:
            self.top = style['top']
        if 'width' in style:
            self.width = style['width']
        if 'height' in style:
            self.height = style['height']
        if 'background-color' in style:
            self.background_color = style['background-color']

        if 'padding-left' in style:
            self.padding_left = style['padding-left']

        if 'padding-top' in style:
            self.padding_top = style['padding-top']

        if 'padding-right' in style:
            self.padding_right = style['padding-right']

        if 'padding-bottom' in style:
            self.padding_bottom = ['padding-bottom']

        if 'padding' in style:
            self.padding = style['padding']

        if len(self.borders.keys()) > 0:
            self.restoreBorders()
        else:
            if 'border-width' in style:
                self.border_width = style['border-width']
            if 'border-radius' in style:
                self.border_radius = style['border-radius']
            if 'border-color' in style:
                self.border_color = style['border-color']

    @classmethod
    def default_events(cls, id):
        ret = OrderedDict()
        ret['onhover'] = {
            "code": "pass",
            "name": "on_%s_hover" % id
        }
        ret['onenter'] = {
            "code": "pass",
            "name": "on_%s_enter" % id
        }
        ret['onexit'] = {
            "code": "pass",
            "name": "on_%s_exit" % id
        }
        ret['onpress'] = {
            "code": "pass",
            "name": "on_%s_press" % id
        }
        ret['onrelease'] = {
            "code": "pass",
            "name": "on_%s_release" % id
        }
        ret['onclick'] = {
            "code": "pass",
            "name": "on_%s_click" % id
        }
        ret['onrightclick'] = {
            "code": "pass",
            "name": "on_%s_rightclick" % id
        }
        ret['ondoubleclick'] = {
            "code": "pass",
            "name": "on_%s_doubleclick" % id
        }
        ret['onlongpress'] = {
            "code": "pass",
            "name": "on_%s_longpress" % id
        }
        return ret

    @classmethod
    def defaut_style(cls):
        return {
            "left": 0,
            "top": 0,
            "width": 64,
            "height": 64,
            "border-width": 0,
            "border-color": "transparent",
            "border-radius": 0,
            "background-color": "#282828",
        }

    @classmethod
    def defaut_attributes(cls):
        return {
            "style": cls.defaut_style()
        }

    @staticmethod
    def defaut_json(cls, etype="div", left=0, top=0):
        node = {
            "type": etype,
            "attributes": cls.defaut_attributes(),
            "nodes": [],
            "bindings": [],
            "events": []
        }
        node["attributes"]["style"]["left"] = left
        node["attributes"]["style"]["top"] = top
        return node
