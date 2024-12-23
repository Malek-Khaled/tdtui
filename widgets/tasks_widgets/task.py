import urwid


class Task(urwid.SelectableIcon):
    def __init__(self, task, color, main_frame, *args):
        self.main_frame = main_frame
        self.is_completed = False
        self.task = task
        self.icons = {"completed": "", "not_completed": ""}
        self.color = color
        self.task_color_map = urwid.AttrMap(self, self.color, f"{self.color}_focus")
        self.task_completed_color_map = urwid.AttrMap(
            self, "task_completed", "task_completed_focus"
        )
        super().__init__(*args, text=f"{self.get_status()} {self.task}")

    def get_status(self):
        if self.is_completed:
            return self.icons["completed"]
        else:
            return self.icons["not_completed"]

    def change_status(self):
        self.is_completed = not self.is_completed
        self.set_text(f"{self.get_status()} {self.task}")
        self.change_group()

    def change_group(self):
        if self.is_completed:
            self.main_frame.tasks_list.completed_tasks.list_walker.append(
                self.task_completed_color_map
            )
            self.main_frame.tasks_list.incompleted_tasks.list_walker.pop(
                self.main_frame.tasks_list.incompleted_tasks.list_box.focus_position
            )
        else:
            self.main_frame.tasks_list.incompleted_tasks.list_walker.append(
                self.task_color_map
            )
            self.main_frame.tasks_list.completed_tasks.list_walker.pop(
                self.main_frame.tasks_list.completed_tasks.list_box.focus_position
            )
        self.main_frame.tasks_list.auto_focus()

    def keypress(self, size, key):
        if key == "enter":
            self.change_status()
        return super().keypress(size, key)
