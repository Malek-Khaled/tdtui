import urwid
from widgets.input_widgets.add_task import Add_task
from widgets.tasks_widgets.tasks_list import Tasks_list


class Main_frame(urwid.Frame):
    def __init__(self, *args):
        self.tasks_list = Tasks_list(self)
        self.task_def = Add_task(self.tasks_list.incompleted_tasks.list_walker, self)
        self.main_layout = urwid.Pile(
            [("weight", 2, self.tasks_list), ("fixed", 3, self.task_def)]
        )
        super().__init__(self.main_layout, *args)
        self.main_layout.set_focus(self.task_def)

    def keypress(self, size, key):
        if key in ("q", "Q"):
            self.set_body(self.tasks_list)
        elif key == "tab":
            if self.main_layout.get_focus() == self.task_def:
                if len(self.tasks_list.incompleted_tasks.list_walker) != 0:
                    self.main_layout.set_focus(self.tasks_list)
                    self.tasks_list.set_focus(self.tasks_list.incompleted_tasks)
                elif len(self.tasks_list.completed_tasks.list_walker) != 0:
                    self.main_layout.set_focus(self.tasks_list)
                    self.tasks_list.set_focus(self.tasks_list.completed_tasks)
            else:
                self.main_layout.set_focus(self.task_def)
        else:
            return super().keypress(size, key)


def padding(widget, left=5, right=5):
    return urwid.Padding(widget, left=left, right=right)


palette = [
    ("task_yellow", "yellow", ""),
    ("task_yellow_focus", "black", "yellow"),
    ("task_blue", "light blue", ""),
    ("task_blue_focus", "black", "light blue"),
    ("task_cyan", "light cyan", ""),
    ("task_cyan_focus", "black", "light cyan"),
    ("task_dark_cyan", "dark cyan", ""),
    ("task_dark_cyan_focus", "black", "dark cyan"),
    ("task_green", "light green", ""),
    ("task_green_focus", "black", "light green"),
    ("task_brown", "brown", ""),
    ("task_brown_focus", "black", "brown"),
    ("task_red", "light red", ""),
    ("task_red_focus", "black", "light red"),
    ("task_magenta", "light magenta", ""),
    ("task_magenta_focus", "black", "light magenta"),
    ("task_completed", "dark gray", ""),
    ("task_completed_focus", "black", "dark gray"),
]
main_frame = Main_frame()
loop = urwid.MainLoop(padding(main_frame), palette=palette)

loop.run()
