import urwid
from widgets.tasks_widgets.task import Task


class Select_color(urwid.LineBox):
    def __init__(self, name, main_widget, list_walker, main_frame, *args):
        self.main_frame = main_frame
        self.list_walker = list_walker
        self.task_name = name
        self.main_widget = main_widget
        self.colors = [
            "yellow",
            "magenta",
            "cyan",
            "dark_cyan",
            "green",
            "brown",
            "red",
            "blue",
        ]
        self.colors_attrmap = urwid.SimpleListWalker(
            [self.icon_color(color) for color in self.colors]
        )
        self.colors_list_box = urwid.ListBox(self.colors_attrmap)
        self.color_dict = {i: f"task_{self.colors[i]}" for i in range(len(self.colors))}
        super().__init__(
            *args,
            original_widget=self.colors_list_box,
            title="Select a color",
            title_align="left",
        )

    def keypress(self, size, key):
        if key == "enter":
            task = Task(
                self.task_name.input.get_edit_text(),
                self.color_dict[self.colors_list_box.focus_position],
                self.main_frame,
            )
            self.main_frame.save_state.data["tasks"][
                self.task_name.input.get_edit_text()
            ] = self.color_dict[self.colors_list_box.focus_position]
            self.main_frame.save_state.save()
            self.set_add_task_mode()
            self.colors_list_box.set_focus(0)
            self.list_walker.append(task.task_color_map)
        elif key in ("k", "K", "up"):
            self.focus_previous()
        elif key in ("j", "J", "down"):
            self.focus_next()
        else:
            return super().keypress(size, key)

    def focus_next(self):
        if self.colors_list_box.focus_position < len(self.colors_attrmap) - 1:
            self.colors_list_box.focus_position += 1

    def focus_previous(self):
        if self.colors_list_box.focus_position > 0:
            self.colors_list_box.focus_position -= 1

    def icon_color(self, color):
        icon_text = urwid.Text("")
        return urwid.AttrMap(icon_text, f"task_{color}", f"task_{color}_focus")

    def set_add_task_mode(self):
        self.main_widget.set_body(self.task_name)
        self.task_name.input.set_edit_text("")
        self.main_frame.set_body(self.main_frame.main_layout)
        self.main_frame.main_layout.set_focus(self.main_frame.task_def)
