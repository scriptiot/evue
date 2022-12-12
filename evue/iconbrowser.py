# -*- coding: utf-8 -*-
import re
import functools
from itertools import cycle
from threading import Timer
from collections import defaultdict
from functools import cached_property
from typing import Any, Callable, List

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
    GridView,
    ButtonStyle,
    SnackBar,
    TextField,
    Switch
)
from flet.padding import Padding
from flet.control_event import ControlEvent


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


class Sidebar(UserControl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, expand=True)
        self.menu = Column(
            auto_scroll=True,
            width=200,
        )

    def add(self, *item: Any):
        self.menu.controls.extend(item)
        self.update()

    def build(self):
        return self.menu


class SearchApp(UserControl):
    def __init__(self, app, max_count: int = 200, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.max_count = max_count
        self.text = TextField(height=35, icon=icons.SEARCH, border_radius=17.5, content_padding=Padding(
            15, 2, 0, 2
        ), opacity=0.5, on_change=self.on_search)
        self.switch = Switch(label="light", on_change=self.theme_changed)
        self.row = Row([
            Row([
                self.text,
                TextButton(text="Search", on_click=self.on_search),
            ], alignment="center", vertical_alignment="start", expand=True
            ),
            self.switch

        ], height=50, alignment="center", vertical_alignment="start")

    def theme_changed(self, e):
        self.page.theme_mode = "dark" if self.page.theme_mode == "light" else "light"
        self.switch.label = "Dark" if self.page.theme_mode == "dark" else "Light"
        self.update()
        self.page.update()

    def build(self):
        return self.row

    @debounce(0.3)
    def on_search(self, e: ControlEvent):
        icon = []
        if (search := self.text.value) and len(search) >= 2:
            count = 0
            for values in self.app.icons.values():
                for value in values:
                    if re.search(search, value, re.IGNORECASE):
                        icon.append(value)
                        count += 1
                        if count >= self.max_count:
                            self.app.show_icons(icon)
                            return
        self.app.show_icons(icon)


class IconExplore(Container):
    def __init__(self, page:Page):
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
            max_extent=150,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,
        )

    @cached_property
    def icons(self):
        data = defaultdict(list)
        for key in icons.__dict__.keys():
            if key.startswith('_') or not key[0].isupper():
                continue
            key_prefix = key.split("_")[0]
            data[key_prefix].append(key)
        return dict(sorted(data.items(), key=lambda x: (x[0][0], len(x[0]))))

    def color(self):
        return next(self.__colors)

    def copy_code(self, e: ControlEvent):
        for widget in e.control.content.controls:
            if isinstance(widget, Text):
                text = "icons.%s" % widget.value
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

    def show_icons(self, values: List[str]) -> None:
        self.container.controls.clear()
        self.page.update()
        for index, key in enumerate(values, start=1):
            self.container.controls.append(
                Container(
                    content=Column([
                        IconButton(icon=getattr(icons, key), icon_size=64),
                        Text("%s" % key, color="#ffffff", visible=False)
                    ],
                        expand=True,
                        alignment="center",
                        horizontal_alignment="center",
                        width=120
                    ), width=200, border=None,
                    # bgcolor=self.color(),
                    on_hover=self.visible_text,
                    on_click=self.copy_code
                )
            )
            if index % 100 == 0:
                self.page.update()
        self.page.update()
    
    def _build(self):
        def switch(e):
            [setattr(v, "style", None) for v in sidebar.controls]
            e.control.style = ButtonStyle(bgcolor="#35698f", color="#ffffff")
            if values := self.icons.get(e.control.text):
                self.show_icons(values)

        sidebar = ListView(
            controls=[TextButton(prefix, on_click=switch, left=True) for prefix in self.icons],
            width=120
        )
        search = SearchApp(self)

        self.content=Column([
                search,
                Row([
                    sidebar, VerticalDivider(visible=True, width=1, color="#232323"), self.container
                ], expand=True)
            ], expand=True)
        self.expand = True

def main(page: Page):
    dialog = IconExplore(page)
    page.theme_mode = "light"
    page.expand = True
    page.window_center()
    page.add(dialog)
    page.update()

if __name__ == '__main__':
    flet.app(target=main)
