import urwid


class Completed_tasks_list(urwid.LineBox):
    def __init__(self, *args):
        self.list_walker = urwid.SimpleListWalker([])
        self.list_box = urwid.ListBox(self.list_walker)
        super().__init__(*args, original_widget=self.list_box, title="Completed Tasks")
