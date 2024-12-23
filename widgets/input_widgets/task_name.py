import urwid


class Task_name(urwid.LineBox):
    def __init__(self, main_widget, main_frame, *args):
        self.main_frame = main_frame
        self.main_widget = main_widget
        self.input = urwid.Edit(multiline=False)
        self.existing_tasks = []
        super().__init__(
            *args, original_widget=self.input, title="Add a task", title_align="left"
        )

    def keypress(self, size, key):
        if key == "enter":
            self.main_widget.set_body(self.main_widget.set_color)
        elif key == "esc":
            raise urwid.ExitMainLoop()

        elif len(self.input.get_edit_text()) < 30:
            super().keypress(size, key)
