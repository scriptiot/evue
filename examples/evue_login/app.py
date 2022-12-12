# -*- coding: utf-8 -*-
from evue import EvueApp, globalThis, Router
import os
from loguru import logger

def onCreate(config):
    logger.info("app onCreate")

def onDestroy():
    logger.info("app onDestroy")

EvueApp({
    'title': 'Evue',
    'theme_mode': 'light',
    'appDir': os.path.dirname(__file__),
    'onCreate': onCreate,
    'onDestroy': onDestroy,
    'paths': [os.path.dirname(__file__)],
    'uri': "evue_login",
})
