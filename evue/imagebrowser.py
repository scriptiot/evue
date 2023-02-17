# -*- coding: utf-8 -*-
import re
import functools
from itertools import cycle
from threading import Timer
from collections import defaultdict
from functools import cached_property
from typing import Any, Callable, List
import os
from loguru import logger

import pyperclip
import flet
from flet import (
    ListView,
    Page,
    Text,
    UserControl,
    Column,
    icons,
    Container,
    Row,
    VerticalDivider,
    TextButton,
    IconButton,
    FilePicker,
    FilePickerResultEvent,
    Image,
    GridView,
    ButtonStyle,
    SnackBar,
    TextField,
    Switch,
    border_radius,
    border
)
from flet.padding import Padding
from flet.control_event import ControlEvent
import shutil
from os import startfile


class debounce:  # noqa
    def __init__(self, timeout: float = 1):
        self.timeout = timeout
        self._timer = None

    def __call__(self, func: Callable):
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            if self._timer is not None:
                self._timer.cancel()
            self._timer = Timer(self.timeout, func, args=args, kwargs=kwargs)
            self._timer.start()

        return decorator

class SearchApp(UserControl):
    def __init__(self, app, max_count: int = 200, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.max_count = max_count
        self.importButton = TextButton("导入", width=128, height=40)
        self.exploreButton = TextButton("浏览...", width=128, height=40)
        self.text = TextField(height=35, icon=icons.SEARCH, border_radius=17.5, content_padding=Padding(
            15, 2, 0, 2
        ), opacity=0.5, on_change=self.on_search)
        self.switch = Switch(label="light", on_change=self.theme_changed)
        self.row = Row([
            self.importButton,
            Row([
                self.text,
                TextButton(text="Search", on_click=self.on_search),
            ], alignment="center", vertical_alignment="start", expand=True
            ),
            self.exploreButton,
            self.switch
        ], height=50, alignment="center", vertical_alignment="start")

    def theme_changed(self, e):
        self.page.theme_mode = "dark" if self.page.theme_mode == "light" else "light"
        self.switch.label = "Dark" if self.page.theme_mode == "dark" else "Light"
        for c in self.app.container.controls:
            if self.page.theme_mode == "dark":
                c.border = border.all(1, "white")
            else:
                c.border = border.all(1, "black")
        self.update()
        self.page.update()

    def build(self):
        return self.row

    @debounce(0.3)
    def on_search(self, e: ControlEvent):
        icon = []
        if (search := self.text.value) and len(search) >= 2:
            count = 0
            for values in self.app.images.values():
                for value in values:
                    if re.search(search, value, re.IGNORECASE):
                        icon.append(value)
                        count += 1
                        if count >= self.max_count:
                            self.app.show_images(icon)
                            return
        self.app.show_images(icon)


class ImageExplore(Container):
    def __init__(self, page:Page, assets_dir:str):
        super().__init__()
        self.page = page
        self.__colors = cycle(
            ['#fbb4ae', '#b3cde3', '#ccebc5', '#decbe4', '#fed9a6', '#ffffcc', '#e5d8bd', '#fddaec', '#f2f2f2',
             '#b3e2cd', '#fdcdac', '#cbd5e8', '#f4cae4', '#e6f5c9', '#fff2ae', '#f1e2cc', '#cccccc', '#8dd3c7',
             '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462', '#b3de69', '#fccde5', '#d9d9d9', '#bc80bd',
             '#ccebc5', '#ffed6f'])
        self.container = GridView(
            expand=1,
            runs_count=5,
            max_extent=128,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,
        )
        self.get_directory_dialog = FilePicker(on_result=self.get_directory_result)
        self.page.overlay.extend([self.get_directory_dialog])
        self.assets_dir = assets_dir
        self.currentDirName = "/"

    @property
    def keys(self):
        start = len(self.assets_dir)
        d = list(self.images.keys())
        ret = {}
        for item in d:
            if item[start:] == "":
                ret["/"] = item
            else:
                ret[item[start:]] = item
        return ret

    @property
    def images(self):
        rootDir = self.assets_dir
        data = {
            rootDir : []
        }

        def walk(fdir):
            for f in os.listdir(fdir):
                _f = "%s/%s" % (fdir, f)
                if os.path.isdir(_f):
                    if _f not in data:
                        data[_f] = []
                    walk(_f)
                else:
                    data[fdir].append(_f)

        for f in os.listdir(rootDir):
            _f = "%s/%s" % (rootDir, f)
            if os.path.isdir(_f):
                if _f not in data:
                    data[_f] = []
                walk(_f)
            else:
                data[rootDir].append(_f)
        
        
        return data

    def color(self):
        return next(self.__colors)

    def copy_code(self, e: ControlEvent):
        for widget in e.control.content.controls:
            if isinstance(widget, Text):
                if self.currentDirName == "/":
                    text = "%s/%s" % (self.assets_dir, widget.value)
                else:
                    text = "%s%s/%s" % (self.assets_dir, self.currentDirName ,widget.value)
                pyperclip.copy(text)
                e.page.snack_bar = SnackBar(
                    Text(f"Copy code: %s to clipboard" % text,
                         color="white")
                )
                e.page.snack_bar.open = True
                e.page.update()

    def visible_text(self, e: ControlEvent):
        e.control.content.controls[-1].visible = True if e.data == "true" else False
        self.page.update()

    def show_images(self, values: List[str]) -> None:
        self.container.controls.clear()
        self.page.update()
        for index, key in enumerate(values, start=1):
            self.container.controls.append(
                Container(
                    content=Column([
                        Image(src=key,
                            border_radius=border_radius.all(10)
                        ),
                        Text("%s" % os.path.basename(key), visible=False, data="")
                    ],
                        expand=True,
                        alignment="spaceAround",
                        horizontal_alignment="center",
                    ),
                    border = border.all(1, "black"),
                    border_radius=border_radius.all(10),
                    # bgcolor=self.color(),
                    on_hover=self.visible_text,
                    on_click=self.copy_code
                )
            )
            if index % 100 == 0:
                self.page.update()
        
        for c in self.container.controls:
            if self.page.theme_mode == "dark":
                c.border = border.all(1, "white")
            else:
                c.border = border.all(1, "black")
        self.page.update()
    
    def get_directory_result(self, e: FilePickerResultEvent):
        if e.path:
            dname = os.path.basename(e.path)
            newDir = "%s/%s" % (self.assets_dir, dname)
            shutil.copytree(e.path, newDir, dirs_exist_ok=True)
            self.updateSideBar()

    def on_import(self, e):
        self.get_directory_dialog.get_directory_path()
    
    def on_explore(self, e):
        if self.currentDirName == "/":
            d = os.path.abspath(self.assets_dir)
        else:
            d = "%s%s" % (self.assets_dir, self.currentDirName)
            d = os.path.abspath(d)
        startfile(d)

    def updateSideBar(self):
        self.sidebar.controls.clear()
        self.sidebar.controls = [TextButton(prefix, on_click=self.switch, left=True) for prefix in self.keys]
        self.sidebar.update()

    def switch(self, e):
        [setattr(v, "style", None) for v in self.sidebar.controls]
        e.control.style = ButtonStyle(bgcolor="#35698f", color="#ffffff")
        self.currentDirName = e.control.text
        if e.control.text == "/":
            key = self.assets_dir
        else:
            key = "%s%s" % (self.assets_dir, e.control.text)
        if values := self.images.get(key):
            self.show_images(values)

    def showRootDir(self):
        self.sidebar.controls[0].style = ButtonStyle(bgcolor="#35698f", color="#ffffff")
        self.show_images(self.images[self.assets_dir])
        self.update()

    def _build(self):
        self.sidebar = ListView(
            controls=[TextButton(prefix, on_click=self.switch, left=True) for prefix in self.keys],
            width=128
        )
        search = SearchApp(self)
        search.importButton.on_click = self.on_import
        search.exploreButton.on_click = self.on_explore

        self.content=Column([
                search,
                Row([
                    self.sidebar, VerticalDivider(visible=True, width=1, color="#232323"), self.container
                ], expand=True)
            ], expand=True)
        self.expand = True

assets_dir="../../tests/evue_designer/image"

def main(page: Page):
    dialog = ImageExplore(page, assets_dir)
    page.theme_mode = "light"
    page.expand = True
    page.window_center()
    page.add(dialog)
    page.update()

if __name__ == '__main__':
    flet.app(target=main, assets_dir=assets_dir)
