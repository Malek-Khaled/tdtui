import urwid


class Task(urwid.SelectableIcon):
    def __init__(self, task,color, *args):
        self.is_completed = False
        self.task = task
        self.icons = {"completed": "", "not_completed": ""}
        self.color = color
        self.task_color_map = urwid.AttrMap(self, self.color, f'{self.color}_focus')
        super().__init__(*args, text=f"{self.get_status()} {self.task}")
    def get_status(self):
        if self.is_completed:
            return self.icons["completed"]
        else:
            return self.icons["not_completed"]

    def change_status(self):
        self.is_completed = not self.is_completed
        self.set_text(f"{self.get_status()} {self.task}")


    def keypress(self, size, key):
        if key == "enter":
            self.change_status()
        return super().keypress(size, key)
    

class Add_task(urwid.Frame):
    def __init__(self, *args, list_walker):
        self.list_walker = list_walker
        self.input = urwid.Edit(multiline=False)
        self.task_name = task_definition(self)
        self.set_color = Add_color(self.task_name, self, self.list_walker)
        super().__init__(*args, body=self.task_name)


class Add_color(urwid.LineBox):
    def __init__(self, name, main_widget,list_walker,*args):
        self.list_walker = list_walker
        self.task_name = name
        self.main_widget = main_widget
        self.colors_list = urwid.SimpleListWalker([self.icon_color("yellow"),self.icon_color("magenta"), self.icon_color("cyan")])
        self.colors_list_box = urwid.ListBox(self.colors_list)
        self.color_dict = {
            0: "task_yellow",
            1: "task_magenta",
            2: "task_cyan"
        }
        super().__init__(*args, original_widget=self.colors_list_box, title="Select a color", title_align="left")

    def keypress(self, size, key):
        if key == "enter":
            task = Task(self.task_name.input.get_edit_text(), self.color_dict[self.colors_list_box.focus_position])
            self.colors_list_box.set_focus(0)
            self.list_walker.append(task.task_color_map)
            self.main_widget.set_body(self.task_name)
            self.task_name.input.set_edit_text("")
        elif key in ("j", "J","down"):
            self.focus_previous()
        elif key in ("k", "K","up"):
            self.focus_next()
        else:
            return super().keypress(size,key)

    def focus_next(self):
        if self.colors_list_box.focus_position < len(self.colors_list) - 1:
            self.colors_list_box.focus_position += 1

    def focus_previous(self):
        if self.colors_list_box.focus_position > 0:
            self.colors_list_box.focus_position -= 1
    def icon_color(self,color):
        icon_text = urwid.Text("")
        return urwid.AttrMap(icon_text, f"task_{color}", f"task_{color}_focus")

class task_definition(urwid.LineBox):
    def __init__(self,main_widget, *args ):
        self.main_widget = main_widget
        self.input = urwid.Edit(multiline=False)
        super().__init__(*args, original_widget=self.input, title="Add a task", title_align="left")
    def keypress(self, size, key):
        if key == "enter":
            self.main_widget.set_body(self.main_widget.set_color)
        elif key == "esc":
            raise urwid.ExitMainLoop()
        else:
            if len(self.input.get_edit_text()) < 30:
                return super().keypress(size,key)

class Tasks_list(urwid.ListBox):
    def __init__(self, *args):
        self.list_walker = urwid.SimpleListWalker([])
        super().__init__(*args, body=self.list_walker)

    def keypress(self, size, key):
        if key in ("d", "D"):
            self.list_walker.pop(self.focus_position)
        elif key in ("j", "J","down"):
            self.focus_previous()
        elif key in ("k", "K","up"):
            self.focus_next()
        elif key == "tab":
            main_layout.set_focus(input)
        elif key == "esc":
            raise urwid.ExitMainLoop()
        else:
            super().keypress(size,key)

    def focus_next(self):
        if self.focus_position < len(self.list_walker) - 1:
            self.focus_position += 1

    def focus_previous(self):
        if self.focus_position > 0:
            self.focus_position -= 1

def main_keypress(key):
    if key == "tab":
        if main_layout.get_focus() == input:
            main_layout.set_focus(tasks_box)

palette = [
    ("task_yellow", "yellow", ""),
    ("task_yellow_focus", "black", "yellow"),
    ('task_blue', 'dark blue', ""),
    ('task_cyan', 'dark cyan', ""),
    ("task_cyan_focus", "black", "dark cyan"),
    ("task_magenta", "light magenta", ""),
    ('task_magenta_focus', 'black', 'light magenta'),
]

tasks_list = Tasks_list()
input = Add_task(list_walker=tasks_list.list_walker)
tasks_box = urwid.LineBox(tasks_list,title="Tasks", title_align="left")
main_layout = urwid.Pile([("weight", 1,tasks_box), ("fixed",3,input)])
main_layout.set_focus(input)
footer = urwid.Text("")
frame = urwid.Frame(main_layout, footer=footer)
padding = urwid.Padding(frame, right=5, left=5)
loop = urwid.MainLoop(padding, unhandled_input=main_keypress, palette=palette)

loop.run()



