import urwid
from widgets.color import Color
from widgets.task_input import Task_input


class Task_properties(urwid.Overlay):
    def __init__(self, task, main_frame, mode="color", *args):
        self.focused_task = task
        self.mode = mode
        if self.mode == "color":
            self.propertie = Color()
            self.propertie.set_title("Change Color")
            self.size = {"height": 10, "width": 30}
        elif self.mode == "reword":
            self.propertie = Task_input()
            self.propertie.set_title("Reword")
            self.size = {"height": 3, "width": 50}
        self.main_frame = main_frame

        super().__init__(
            *args,
            bottom_w=self.main_frame.main_layout,
            top_w=self.propertie,
            align="center",
            width=self.size["width"],
            height=self.size["height"],
            valign="middle",
        )

    def keypress(self, size, key):
        if key in ("q", "Q", "esc"):
            self.main_frame.set_body(self.main_frame.main_layout)

        elif key == "enter":
            if self.mode == "color":
                self.focused_task.change_color(
                    self.propertie.color_dict[
                        self.propertie.colors_list_box.focus_position
                    ]
                )
            elif self.mode == "reword":
                self.focused_task.reword(self.propertie.input.get_edit_text())

            self.main_frame.set_body(self.main_frame.main_layout)

        return super().keypress(size, key)
