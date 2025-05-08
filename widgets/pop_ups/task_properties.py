from typing import Coroutine
import urwid
from widgets.color import Color


class Task_properties(urwid.Overlay):
    def __init__(self, task, main_frame, *args):
        self.focused_task = task
        self.color = urwid.ScrollBar(
            Color(), thumb_char=urwid.ScrollBar.Symbols.DRAWING_HEAVY
        )
        self.color_selector = self.color.original_widget
        self.color_selector.set_title("Change Color")
        self.main_frame = main_frame

        super().__init__(
            *args,
            bottom_w=self.main_frame.main_layout,
            top_w=self.color,
            align="center",
            width=("relative", 50),
            height=("relative", 40),
            valign="middle",
        )

    def keypress(self, size, key):
        if key in ("q", "Q"):
            self.main_frame.set_body(self.main_frame.main_layout)

        elif key == "enter":
            self.focused_task.change_color(
                self.color_selector.color_dict[
                    self.color_selector.colors_list_box.focus_position
                ]
            )
            self.main_frame.set_body(self.main_frame.main_layout)

        return super().keypress(size, key)
