# -*- coding: utf-8 -*-
from typing import (
    Any,
    Dict
)
from flet import icons
from flet.types import TextAlign
from PIL import ImageFont
from loguru import logger
import traceback
from ..globalthis import globalThis
from ..sessionobject import SessionObject


def getChinese(word:str):
    '''
     判断一个词是否是非英文词,只要包含一个中文，就认为是非英文词汇
     :param word:
     :return:
    '''
    count = 0
    ch_str = ""
    en_str = ""
    for s in word.encode('utf-8').decode('utf-8'):
        if u'\u4e00' <= s <= u'\u9fff':
            count += 1
            ch_str += s
        else:
            en_str += s
    return ch_str, en_str


class BaseElement(Dict[str, Any], SessionObject):

    enableUpdate = True
    
    def __init__(self, sessionID=None) -> None:
        super().__init__()
        self.sessionID = sessionID
        self._font_ = None
        self.userData = None

        # public
        self['width'] = 0
        self['height'] = 0
        self['left'] = 0
        self['top'] = 0
        self['visible'] = True
        # div
        self['border_width'] = 0
        self['border_radius'] = 0
        self['border_color'] = "transparent"
        self['background_color'] = "white"
        # image 
        self['src'] = ""
        # text
        self['value'] = ""
        self['text_align'] = "center"
        self['font_family'] = None
        self['font_size'] = 20
        self['size'] = None
        self['weight'] = None
        self['italic'] = None
        self['style'] = None
        self['max_lines'] = None
        self['overflow'] = None
        self['selectable'] = None
        self['no_wrap'] = None
        self['color'] =  None
        self['background_color'] =  None
        self['semantics_label'] = None
        self['opacity'] = 0
        self['rotate'] = 0
        self['scale'] = 1
        self['offset'] = 0
        self['padding_left'] = 0
        self['padding_top'] = 0
        self['padding_right'] = 0
        self['padding_bottom'] = 0
        self['padding'] = 0

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)
        except:
            return None

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = value
        _name = name.replace("-", "_")
        funcName = "set_%s" % _name
        if hasattr(self, funcName):
            func = getattr(self, funcName)
            func(value)
        else:
            if hasattr(self, "obj") and self.obj:
                setattr(self.obj, _name, value)
        try:
            if BaseElement.enableUpdate:
                self.update()
        except:
            pass

    @classmethod
    def bool(cls, value):
        if isinstance(value, str):
            if value == "true" or value == "True":
                return True
            else:
                return False
        else:
            return bool(value)

    @classmethod
    def textAlign(cls, value):
        if value == TextAlign.NONE:
            return "None"
        return value

    @classmethod
    def alignment(cls, value):
        if value == "left":
            return "start"
        elif value == "right":
            return "end"
        else:
            return value
    
    @classmethod
    def ficon(cls, value):
        if value.startswith("icons."):
            name = value[6:]
            if hasattr(icons, name):
                return getattr(icons, name)
        return None

    def measureText(self, value, size=20):
        if self.sessionID is None:
            return None, None
        if self.page and self.page.theme and self.page.theme.font_family:
            value = str(value)
            try:
                if self._font_ is None:
                    self._font_ = ImageFont.truetype(self.page.theme.font_family, size=20)
                if size:
                    self._font_ = ImageFont.truetype(self.page.theme.font_family, size=size)
                ch, en = getChinese(value)
                if value == en:
                    box = self._font_.getbbox(value)
                    width = box[2] * 1.2
                    height = box[3] * 1.7
                else:
                    chbox = self._font_.getbbox(ch)
                    enbox = self._font_.getbbox(en)
                    width = chbox[2] * 1.7 + enbox[2] * 1.2
                    height = chbox[3] * 1.7
                return width, height
            except:
                logger.warning(traceback.format_exc())
        return None, None

    

