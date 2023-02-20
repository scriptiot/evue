# -*- coding: utf-8 -*-
from typing import (
    Any,
    Dict
)
from loguru import logger

class DataBinding(dict):

    def __init__(self, data, parent=None) -> None:
        super().__init__()
        self['_bindings_'] = {}
        self['_parent_'] = parent
        self.update(data)

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = value

        if name in self['_bindings_']:
            bindings = self['_bindings_'][name]
            for binding in bindings:
                element = binding['element']
                attr = binding['attr']
                setattr(element, attr, value)
                attrHook = "onPropertyChanged_%s" % binding["key"]
                if hasattr(self['_parent_'], attrHook):
                    getattr(self['_parent_'], attrHook)(value)

    def set_binding_value(self, element, attr, key):
        if key not in self['_bindings_']:
            self['_bindings_'][key] = []

        self['_bindings_'][key].append({
            "element": element,
            "attr": attr,
            "key": key
        })
