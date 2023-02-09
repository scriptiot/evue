# -*- coding: utf-8 -*-
from .widgets import *
from .fletbaseelement import *
from .windowtitlebar import WindowtitlebarElement
from .div import DivElement
from .column import ColumnElement
from .stackview import StackViewElement
from .row import RowElement
from .responsiverow import ResponsiveRowElement
from .grid import GridElement
from .collapsible import CollapsibleElement
from .image import ImageElement
from .icon import IconElement
from .iconbutton import IconButtonElement
from .textfield import TextFieldElement
from .textarea import TextareaElement
from .text import TextElement
from .counter import CounterElement
from .button import ButtonElement
from .slider import SliderElement
from .dialog import DialogElement
from .checkbox import CheckboxElement
from .switch import SwitchElement
from .progress import ProgressElement
from .slider import SliderElement
from .combobox import ComboboxElement
from .qrcode import QRCodeElement, qrcode_make_png
from .canvas import CanvasElement
from .listview import ListViewElement
from .listitem import ListItemElement
from .tabview import TabViewElement
from .tab import TabElement
from .markdown import MarkdownElement
from .arc import ArcElement


ElementClass = {
    "windowtitlebar": WindowtitlebarElement,
    "div": DivElement,
    "column": ColumnElement,
    "stackview": StackViewElement,
    "row": RowElement,
    "responsiverow": ResponsiveRowElement,
    "grid": GridElement,
    "collapsible": CollapsibleElement,
    "image": ImageElement,
    "icon": IconElement,
    "iconbutton": IconButtonElement,
    "textfield": TextFieldElement,
    "textarea": TextareaElement,
    "text": TextElement,
    "counter": CounterElement,
    "button": ButtonElement,
    "slider": SliderElement,
    "dialog": DialogElement,
    "checkbox": CheckboxElement,
    "switch": SwitchElement,
    "progress": ProgressElement,
    "slider": SliderElement,
    "combobox": ComboboxElement,
    "qrcode": QRCodeElement,
    "canvas": CanvasElement,
    "listview": ListViewElement,
    "listitem": ListItemElement,
    "tabview": TabViewElement,
    "tab": TabElement,
    "markdown": MarkdownElement,
    "arc": ArcElement
}

UserElements = {}

def getCreator(_type):
    _type = _type.lower()
    if _type in ElementClass:
        EClass = ElementClass[_type]
        return EClass.__name__
    elif _type in UserElements:
        return UserElements[_type]
    else:
        import evue
        return "%s" % evue.componentManager.getComponentName(_type)

def registerElement(name, _class_):
    ElementClass[name] = _class_
    import evue
    setattr(evue, _class_.__name__, _class_)

def registerUserElement(name, classname):
    UserElements[name] = classname
