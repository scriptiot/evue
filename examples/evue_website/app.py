# -*- coding: utf-8 -*-
from evue import EvueApp, globalThis
import os

def registerComponents(appDir):
    pass

def onCreate(config):
    registerComponents(config['appDir'])

def onDestroy():
    pass

globalThis.project = {'assets_dir': './', 'host': None, 'port': None, 'view': 'desktop', 'web_renderer': 'canvas', 'dir': './evue_website', 'entry': 'evue_website'}
globalThis.project['assets_dir'] = os.path.dirname(__file__)
globalThis.project['root_dir'] =  os.path.dirname(os.path.dirname(__file__))
globalThis.project['dir'] = os.path.dirname(__file__)
globalThis.project['projectJson'] = "%s/project.json" % os.path.dirname(__file__)

EvueApp({
    'appDir': os.path.dirname(__file__),
    'onCreate': onCreate,
    'onDestroy': onDestroy,
    'paths': [os.path.dirname(__file__)],
    'uri': globalThis.project['entry'],
})