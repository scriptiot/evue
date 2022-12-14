# -*- coding: utf-8 -*-
from evue import EvueApp, globalThis
import os
from loguru import logger

def onCreate(config):
    logger.info("app onCreate")

def onDestroy():
    logger.info("app onDestroy")

globalThis.project = {
    "assets_dir": os.path.dirname(__file__),
    "host": None,
    "port": None,
    "view": "desktop",
    "web_renderer": "canvas",
    "dir": os.path.dirname(__file__),
    "entry": "evue_website",
}

EvueApp({
    'title': 'Evue',
    'theme_mode': 'light',
    'appDir': os.path.dirname(__file__),
    'paths': [os.path.dirname(__file__)],
    'onCreate': onCreate,
    'onDestroy': onDestroy,
    'uri': globalThis.project['entry'],
})
