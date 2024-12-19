import urwid


class Task(urwid.SelectableIcon):
    def __init__(self, task,color, *args):
        self.is_completed = False
        self.task = task
        self.icons = {"completed": "", "not_completed": ""}
        self.color = color
        self.task_color_map = urwid.AttrMap(self, self.color, f'{self.color}_focus')
        self.task_completed_color_map = urwid.AttrMap(self, "task_completed", "task_completed_focus")
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
            tasks_list.completed_tasks.list_walker.append(self.task_completed_color_map)
            tasks_list.incompleted_tasks.list_walker.pop(tasks_list.incompleted_tasks.list_box.focus_position)
        else:

            tasks_list.incompleted_tasks.list_walker.append(self.task_color_map)
            tasks_list.completed_tasks.list_walker.pop(tasks_list.completed_tasks.list_box.focus_position)
        tasks_list.auto_focus()




    def keypress(self, size, key):
        if key == "enter":
            self.change_status()
        return super().keypress(size, key)
    

class Add_task(urwid.Frame):
    def __init__(self, *args, list_walker):
        self.list_walker = list_walker
        self.input = urwid.Edit(multiline=False)
        self.task_name = task_definition(self)
        self.set_color = Select_color(self.task_name, self, self.list_walker)
        super().__init__(*args, body=self.task_name)


class Select_color(urwid.LineBox):
    def __init__(self, name, main_widget,list_walker,*args):
        self.list_walker = list_walker
        self.task_name = name
        self.main_widget = main_widget
        self.colors = ["yellow", "magenta", "cyan", "dark_cyan", "green", "brown", "red", "blue"]
        self.colors_attrmap = urwid.SimpleListWalker([self.icon_color(color) for color in self.colors])
        self.colors_list_box = urwid.ListBox(self.colors_attrmap)
        self.color_dict = {i:f"task_{self.colors[i]}" for i in range(len(self.colors))}
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
        if self.colors_list_box.focus_position < len(self.colors_attrmap) - 1:
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

class Incompleted_tasks_list(urwid.LineBox):
    def __init__(self,*args):
        self.list_walker = urwid.SimpleListWalker([])
        self.list_box = urwid.ListBox(self.list_walker)
        super().__init__(*args, original_widget=self.list_box, title="Tasks")

class Completed_tasks_list(urwid.LineBox):
    def __init__(self, *args):
        self.list_walker = urwid.SimpleListWalker([])
        self.list_box = urwid.ListBox(self.list_walker)
        super().__init__(*args, original_widget=self.list_box, title="Completed Tasks")


class Tasks_list(urwid.Pile):
    def __init__(self, *args):
        self.incompleted_tasks = Incompleted_tasks_list()
        self.completed_tasks = Completed_tasks_list()
        super().__init__(*args, widget_list=[self.incompleted_tasks, self.completed_tasks])

    def keypress(self, size, key):
        try:
            if key in ("d", "D"):
                self.get_listwalker().pop(self.get_focus().list_box.focus_position)
                self.auto_focus()
            elif key in ("j", "J","down"):
                self.focus_previous()
            elif key in ("k", "K","up"):
                self.focus_next()
            elif key in ("e","E"):
                if self.get_focus() == self.incompleted_tasks and len(self.completed_tasks.list_walker) != 0:
                    self.set_focus(self.completed_tasks)
                elif len(self.incompleted_tasks.list_walker) != 0:
                    self.set_focus(self.incompleted_tasks)
            elif key == "tab":
                    main_layout.set_focus(input)
            elif key == "esc":
                raise urwid.ExitMainLoop()
            else:
                super().keypress(size,key)
        except IndexError:
            pass

    def focus_next(self):
        if self.get_focus().list_box.focus_position < len(self.get_listwalker()) - 1:
            self.get_focus().list_box.focus_position += 1

    def focus_previous(self):
        if self.get_focus().list_box.focus_position > 0:
            self.get_focus().list_box.focus_position -= 1

    def get_listwalker(self, unfocused=False):
        if self.get_focus() == self.incompleted_tasks and not unfocused:
            return self.incompleted_tasks.list_walker
        elif self.get_focus() != self.incompleted_tasks and unfocused:
            return self.incompleted_tasks.list_walker
        elif self.get_focus() == self.completed_tasks and not unfocused:
            return self.completed_tasks.list_walker
        else:
            return self.completed_tasks.list_walker

    def auto_focus(self):
        if len(self.get_listwalker()) == 0 and len(self.get_listwalker(unfocused=True)) != 0:
            self.set_focus(self.get_unfocused())
            

        elif len(self.get_listwalker()) == 0 and len(self.get_listwalker(unfocused=True)) == 0:
            main_layout.set_focus(input)

    def get_unfocused(self):
        if self.get_focus() == self.incompleted_tasks:
            return self.completed_tasks
        else:
            return self.incompleted_tasks

def main_keypress(key):
    if key == "tab":
        if main_layout.get_focus() == input:
            main_layout.set_focus(tasks_box)
            tasks_list.set_focus(tasks_list.incompleted_tasks)

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
    ("task_completed_focus", "black", "dark gray")
]

tasks_list = Tasks_list()
input = Add_task(list_walker=tasks_list.incompleted_tasks.list_walker)
tasks_box = urwid.LineBox(tasks_list,title="Tasks", title_align="left")
main_layout = urwid.Pile([("weight", 1,tasks_box), ("fixed",3,input)])
main_layout.set_focus(input)
footer = urwid.Text("")
frame = urwid.Frame(main_layout, footer=footer)
padding = urwid.Padding(frame, right=5, left=5)
loop = urwid.MainLoop(padding, unhandled_input=main_keypress, palette=palette)

loop.run()



