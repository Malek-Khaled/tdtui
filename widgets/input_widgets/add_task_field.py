import urwid
from widgets.input_widgets.select_color import Select_color
from widgets.input_widgets.task_name import Task_name


class Add_task_field(urwid.Frame):
    def __init__(self, list_walker, main_frame, *args):
        self.main_frame = main_frame
        self.list_walker = list_walker
        self.input = urwid.Edit(multiline=False)
        self.task_name = Task_name(self, self.main_frame)
        self.set_color = urwid.ScrollBar(
            Select_color(self.task_name, self, self.list_walker, self.main_frame),
            thumb_char=urwid.ScrollBar.Symbols.DRAWING_HEAVY,
        )
        super().__init__(*args, body=self.task_name)
