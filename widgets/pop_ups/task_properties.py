import urwid
from widgets.color import Color
from widgets.task_input import Task_input


class Task_properties(urwid.Overlay):
    def __init__(self, task, main_frame, mode="color", *args):
        self.focused_task = task
        self.mode = mode
        if self.mode == "color":
            self.color = urwid.ScrollBar(
                Color(), thumb_char=urwid.ScrollBar.Symbols.DRAWING_HEAVY
            )
            self.color_selector = self.color.original_widget
            self.color_selector.set_title("Change Color")
            self.propertie = self.color_selector
        elif self.mode == "reword":
            self.propertie = Task_input()
            self.propertie.set_title("Reword")
        self.main_frame = main_frame

        super().__init__(
            *args,
            bottom_w=self.main_frame.main_layout,
            top_w=self.propertie,
            align="center",
            width=("relative", 50),
            height=("relative", 40),
            valign="middle",
        )

    def keypress(self, size, key):
        if key in ("q", "Q", "esc"):
            self.main_frame.set_body(self.main_frame.main_layout)

        elif key == "enter":
            if self.mode == "color":
                self.focused_task.change_color(
                    self.color_selector.color_dict[
                        self.color_selector.colors_list_box.focus_position
                    ]
                )
            elif self.mode == "reword":
                self.focused_task.reword(self.propertie.input.get_edit_text())

            self.main_frame.set_body(self.main_frame.main_layout)

        return super().keypress(size, key)
