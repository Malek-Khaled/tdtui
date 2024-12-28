import urwid


class Task_name(urwid.LineBox):
    def __init__(self, main_widget, main_frame, *args):
        self.main_frame = main_frame
        self.main_widget = main_widget
        self.input = urwid.Edit(multiline=False)
        super().__init__(
            *args, original_widget=self.input, title="Add a task", title_align="left"
        )

    def keypress(self, size, key):
        if key == "enter":
            if (
                self.input.get_edit_text()
                not in self.main_frame.tasks_list.existing_tasks
            ):
                self.main_frame.tasks_list.existing_tasks.append(
                    self.input.get_edit_text()
                )
                self.main_widget.set_body(self.main_widget.set_color)
            else:
                self.main_frame.set_body(self.main_frame.existing_task_error)
        elif key == "esc":
            raise urwid.ExitMainLoop()

        elif len(self.input.get_edit_text()) < 30:
            super().keypress(size, key)
