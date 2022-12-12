# -*- coding: utf-8 -*-
from .globalthis import require

class ComponentManager(object):
    
    def __init__(self) -> None:
        self._usercomponents_ = {}
    
    @property
    def userComponents(self):
        return self._usercomponents_

    def registerComponent(self, componentInfo):
        name = componentInfo['name']
        path = componentInfo['path']
        module = require(path)
        componentInfo['module'] = module
        self.userComponents[name] = componentInfo

    def getComponentName(self, name):
        elementname = "%sComponent" % name.capitalize()
        return elementname

    def getUserComponent(self, name):
        componentName = self.getComponentName(name)
        import evue
        return getattr(evue, componentName)

componentManager = ComponentManager()
