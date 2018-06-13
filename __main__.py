from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, \
    Button, TextBox, Widget, MultiColumnListBox, DatePicker, TimePicker, CheckBox, RadioButtons
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import sys
import sqlite3

import todolist
from todolist.todolistdb import TodoListDB
from todolist.advWidgets import DropdownList, PopUpDialog, PopupMenu

import locale
import datetime
#print(locale.windows_locale.values())
#print(locale.getdefaultlocale())
locale.setlocale(locale.LC_ALL, 'C')
#locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
#locale.setlocale(locale.LC_CTYPE, 'en_US.UTF-8')

class TodoListModel(object):
    def __init__(self):
        self._db = TodoListDB()
        self.current_id = None

        self.filter_finished = 0
        self.filter_due = 0
        self.filter_category = -2

    def add_todo(self, what, due, category, notes, finished):
        return self._db.add_todo(what, due, category, notes, finished)

    def add_category(self, category):
        return self._db.add_category(category)

    def get_summary(self):
        rows = self._db.get_todo()
        if self.filter_finished == 1:
            summary = [((x[1], x[2], x[3], 'Y' if x[5] else 'N'), x[0]) for x in rows if x[5]]
        elif self.filter_finished == 2:
            summary = [((x[1], x[2], x[3], 'Y' if x[5] else 'N'), x[0]) for x in rows if not x[5]]
        else:
            summary = [((x[1], x[2], x[3], 'Y' if x[5] else 'N'), x[0]) for x in rows]

        if self.filter_category == -1:
            summary = [x for x in summary if not x[0][2]]
        elif 0 <= self.filter_category:
            filter_category_str = self._db.get_category("id=" + str(self.filter_category))
            if filter_category_str:
                filter_category_str = filter_category_str[0][1]
                summary = [x for x in summary if x[0][2] == filter_category_str]

        if self.filter_due == 1:
            summary = sorted(summary, key=lambda x: datetime.datetime.strptime(x[0][1], "%Y-%m-%d %H:%M:%S")) 
        elif self.filter_due == 2:
            summary = sorted(summary, key=lambda x: datetime.datetime.strptime(x[0][1], "%Y-%m-%d %H:%M:%S"), reverse=True)

        return summary

    def get_categorys(self):
        rows = self._db.get_category()
        categorys = [(x[1], x[0]) for x in rows]

        return categorys

    def get_todo(self, todo_id):
        row = self._db.get_todo("id=" + str(todo_id))
        if row:
            row = row[0]
        else:
            return None
        id = row[0]
        what = row[1]
        due = row[2]
        due_datetime = datetime.datetime.strptime(due, "%Y-%m-%d %H:%M:%S")
        due_datetime = due_datetime.replace(microsecond=0)
        due_date = due_datetime.date()
        due_time = due_datetime.time()
        category = row[3]
        category = self._db.get_category("name='" + category + "'") if category else None
        category = category[0][0] if category else -1
        notes = row[4]
        finished = row[5]
        todo = {
            "id": id,
            "what": what,
            "due_date": due_date,
            "due_time": due_time,
            "category": category,
            "notes": notes,
            "finished": bool(finished)
        }

        return todo

    def get_current_todo(self):
        if self.current_id is None:
            due_datetime = datetime.datetime.now()
            due_datetime = due_datetime.replace(microsecond=0)
            todo = {
                "id": -1,
                "what": "",
                "due_date": due_datetime.date(),
                "due_time": due_datetime.time(),
                "category": -1,
                "notes": "",
                "finished": False
            }
            return todo
        else:
            return self.get_todo(self.current_id)

    def get_current_categorys(self):
        rows = self._db.get_category()
        categorys = [("", -1)] + [(x[1], x[0]) for x in rows]
        return categorys

    def update_current_todo(self, details):
        id = details["id"]
        what = details["what"]
        what = what.replace("'", "''")
        due = str(details["due_date"]) + " " + str(details["due_time"])
        category = details["category"]
        category = self._db.get_category("id=" + str(category))
        category = category[0][1] if category else ""
        notes = details["notes"]
        notes = notes.replace("'", "''")
        finished = details["finished"]

        if id == -1 and self._db.get_todo("what='" + what + "'"):
            return False

        if self.current_id is None:
            self.add_todo(what, due, category, notes, str(int(finished)))
        else:
            modifys = (
                ("what", what),
                ("due", due),
                ("category", category),
                ("notes", notes),
                ("finished", str(int(finished)))
            )
            self._db.modify_todo(modifys, "id=" + str(id))

        return True

    def delete_todo(self, todo_id):
        if todo_id is not None:
            self._db.remove_todo("id=" + str(todo_id))

    
    def delete_category(self, category_id):
        if category_id is not None:
            self._db.remove_category("id=" + str(category_id))
    
    @staticmethod
    def _valid_string_check(s):
        for c in s:
            c_ord = ord(c)
            if not (
                (ord('A') <= c_ord <= ord('Z')) or
                (ord('a') <= c_ord <= ord('z')) or
                (ord('0') <= c_ord <= ord('9')) or
                (ord('ㄱ') <= c_ord <= ord('ㅣ')) or
                (ord('가') <= c_ord <= ord('ퟻ')) or
                (c in " `~!@#$%^&*()-_=+\\|[]{};:'\",<.>/?")
            ):
                return False
        return True


class ListView(Frame):
    def __init__(self, screen, model):
        super(ListView, self).__init__(screen,
                                       screen.height * 2 // 3,
                                       screen.width * 2 // 3,
                                       on_load=self._reload_list,
                                       hover_focus=True,
                                       title="To-Do List")
        self._model = model

        self.palette["background"] = (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_WHITE)
        self.palette["disabled"] = (Screen.COLOUR_RED, Screen.A_NORMAL, Screen.COLOUR_WHITE)
        self.palette["invalid"] = (Screen.COLOUR_YELLOW, Screen.A_NORMAL, Screen.COLOUR_RED)
        self.palette["label"] = (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_WHITE)
        self.palette["borders"] = (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_WHITE)
        self.palette["scroll"] = (Screen.COLOUR_CYAN, Screen.A_NORMAL, Screen.COLOUR_WHITE)
        self.palette["title"] = (Screen.COLOUR_BLACK, Screen.A_BOLD, Screen.COLOUR_WHITE)
        self.palette["edit_text"] = (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_WHITE)
        self.palette["focus_edit_text"] = (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLUE)
        self.palette["button"] = (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_WHITE)
        self.palette["focus_button"] = (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLUE)
        self.palette["control"] = (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_WHITE)
        self.palette["selected_control"] = (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_WHITE)
        self.palette["focus_control"] = (Screen.COLOUR_YELLOW, Screen.A_NORMAL, Screen.COLOUR_WHITE)
        self.palette["selected_focus_control"] = (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_BLUE)
        self.palette["field"] = (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_WHITE)
        self.palette["selected_field"] = (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_WHITE)
        self.palette["focus_field"] = (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_WHITE)
        self.palette["selected_focus_field"] = (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_BLUE)

        self._list_view = MultiColumnListBox(
            Widget.FILL_FRAME,
            ["35%", "30%", "20%", "15%"],
            model.get_summary(),
            ["<What>", "<Due>", "<category>", "<finished>"],
            name="todo_list",
            on_change=self._on_pick
        )

        self._view_button = Button("View", self._view)
        self._delete_button = Button("Delete", self._delete)
        self._edit_button = Button("Edit", self._edit)
        self._quit_button = Button("Quit", self._quit)

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())

        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(self._view_button, 0)
        layout2.add_widget(self._edit_button, 1)
        layout2.add_widget(self._delete_button, 2)
        layout2.add_widget(self._quit_button, 3)

        self.fix()
        self._on_pick()

    def _on_pick(self):
        self._view_button.disabled = self._list_view.value is None
        self._delete_button.disabled = self._list_view.value is None

    def _reload_list(self, new_value=None):
        self._list_view.options = self._model.get_summary()
        self._list_view.value = new_value

    def _edit(self):
        btn_location = self._edit_button.get_location()
        self._scene.add_effect(
        PopupMenu(
            self._screen,
            [
                ("New Todo", self._new_todo),
                ("Category", self._edit_category),
                ("Filter", self._edit_filter)
            ],
            btn_location[0] + self._edit_button._w , btn_location[1] - (self._edit_button._h * 2))
        )
        #self._model.current_id = None
        #raise NextScene("Todo View")

    def _new_todo(self):
        self._model.current_id = None
        raise NextScene("Todo View")

    def _edit_category(self):
        self._model.current_id = None
        raise NextScene("Category View")

    def _edit_filter(self):
        self._model.current_id = None
        raise NextScene("Filter View")

    def _view(self):
        self.save()
        self._model.current_id = self.data["todo_list"]
        if self._model.current_id:
            raise NextScene("Todo View")

    def _delete(self):
        self.save()
        self._model.delete_todo(self.data["todo_list"])
        self._reload_list()

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")


class TodoView(Frame):
    def __init__(self, screen, model):
        super(TodoView, self).__init__(screen,
                                          screen.height * 2 // 3,
                                          screen.width * 2 // 3,
                                          hover_focus=True,
                                          title="To-Do Details",
                                          reduce_cpu=True)
        self._model = model

        due_datetime = datetime.datetime.now()
        due_datetime = due_datetime.replace(microsecond=0)
        self.data["id"] = -1
        self.data["what"] = ""
        self.data["due_date"] = due_datetime.date()
        self.data["due_time"] = due_datetime.time()
        self.data["category"] = 0
        self.data["finished"] = False

        self._category_ddlist = DropdownList(
            [("", -1)],
            label="Category:",
            name="category"
        )
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("What:", "what"))
        layout.add_widget(DatePicker(
            "Due Date:",
            name="due_date",
            year_range=range(1999, 2100)
            )
        )
        layout.add_widget(TimePicker("Due Time:", name="due_time", seconds=True))
        layout.add_widget(self._category_ddlist)
        layout.add_widget(TextBox(
            Widget.FILL_FRAME, "Notes:", "notes", as_string=True))
        layout.add_widget(CheckBox("", label="Finished:", name="finished"))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def reset(self):
        super(TodoView, self).reset()
        self.data = self._model.get_current_todo()
        self._category_ddlist.options = self._model.get_current_categorys()
        self._category_ddlist.value = self.data["category"]

    def _ok(self):
        self.save()
        if self.data["what"]:
            if (
                self._model._valid_string_check(self.data["what"]) and
                self._model._valid_string_check(self.data["notes"])
            ):
                if self._model.update_current_todo(self.data):
                    raise NextScene("Main")
                else:
                    self._scene.add_effect(
                        PopUpDialog(self._screen, "It already exists!", ["OK"]))
        else:
            self._scene.add_effect(
                PopUpDialog(self._screen, "Please enter what to do!", ["OK"]))

    @staticmethod
    def _cancel():
        raise NextScene("Main")

class CategoryView(Frame):
    def __init__(self, screen, model):
        super(CategoryView, self).__init__(screen,
                                          screen.height * 2 // 3,
                                          screen.width * 2 // 3,
                                          hover_focus=True,
                                          title="Categorys",
                                          reduce_cpu=True)
        self._model = model

        self.data["category"] = ""

        self._list_view = ListBox(
            Widget.FILL_FRAME,
            model.get_categorys(),
            name="categorys",
            on_change=self._on_pick
        )
        
        self._add_button = Button("Add", self._add)
        self._delete_button = Button("Delete", self._delete)
        self._back_button = Button("Back", self._back)

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())

        layout2 = Layout([100])
        self.add_layout(layout2)
        layout2.add_widget(Text("Category:", "category"))
        layout2.add_widget(Divider())

        layout3 = Layout([1, 1, 1, 1])
        self.add_layout(layout3)
        layout3.add_widget(self._add_button, 0)
        layout3.add_widget(self._delete_button, 1)
        layout3.add_widget(self._back_button, 3)

        self.fix()

    def _on_pick(self):
        self._delete_button.disabled = self._list_view.value is None

    def reset(self):
        super(CategoryView, self).reset()

    def _reload_list(self, new_value=None):
        self._list_view.options = self._model.get_categorys()
        self._list_view.value = new_value

    def _add(self):
        self.save()
        if self.data["category"]:
            if self._model._valid_string_check(self.data["category"]):
                if self._model.add_category(self.data["category"]):
                    self._reload_list()
                else:
                    self._scene.add_effect(
                        PopUpDialog(self._screen, "It already exists!", ["OK"]))
        else:
            self._scene.add_effect(
                PopUpDialog(self._screen, "Please enter category name!", ["OK"]))

    def _delete(self):
        self.save()
        self._model.delete_category(self.data["categorys"])
        self._reload_list()

    @staticmethod
    def _back():
        raise NextScene("Main")

class FilterView(Frame):
    def __init__(self, screen, model):
        super(FilterView, self).__init__(screen,
                                          screen.height * 2 // 3,
                                          screen.width * 2 // 3,
                                          hover_focus=True,
                                          title="Filters",
                                          reduce_cpu=True)
        self._model = model

        self.data["filter_finished"] = 0
        self.data["filter_due"] = 0
        self.data["filter_category"] = -2
        
        self._finished_rbutton = RadioButtons(
            [
                ("All", 0),
                ("Finished", 1),
                ("Unfinished", 2)
            ],
            label="Finished:",
            name="filter_finished"
        )
        self._due_rbutton = RadioButtons(
            [
                ("None", 0),
                ("Closest", 1),
                ("Farthest", 2)
            ],
            label="Due Sort:",
            name="filter_due"
        )
        self._category_ddlist = DropdownList(
            [
                ("ALL", -2),
                ("", -1)
            ],
            label="Category:",
            name="filter_category"
        )
        self._apply_button = Button("Apply", self._apply)
        self._back_button = Button("Back", self._back)

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._finished_rbutton)
        layout.add_widget(Divider())
        layout.add_widget(self._due_rbutton)
        layout.add_widget(Divider())
        layout.add_widget(self._category_ddlist)
        layout.add_widget(Divider())
        

        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(self._apply_button, 0)
        layout2.add_widget(self._back_button, 3)

        self.fix()


    def reset(self):
        super(FilterView, self).reset()
        self._category_ddlist.options = [("ALL", -2)] + self._model.get_current_categorys()
        self._category_ddlist.value = self._model.filter_category

    def _apply(self):
        self.save()
        self._model.filter_finished = self.data["filter_finished"]
        self._model.filter_due = self.data["filter_due"]
        self._model.filter_category = self.data["filter_category"]
        raise NextScene("Main")

    @staticmethod
    def _back():
        raise NextScene("Main")

        
def demo(screen, scene):
    screen.clear()
    scenes = [
        Scene([ListView(screen, todos)], -1, name="Main"),
        Scene([TodoView(screen, todos)], -1, name="Todo View"),
        Scene([CategoryView(screen, todos)], -1, name="Category View"),
        Scene([FilterView(screen, todos)], -1, name="Filter View")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene)


todos = TodoListModel()
last_scene = None

def main_loop():
    global last_scene
    while True:
        try:
            Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene

def cmd_add(argv):
    db = TodoListDB()
    if (len(argv) == 2):
        db.add_todo(argv[0], argv[1])
    elif (len(argv) == 3):
        db.add_todo(argv[0], argv[1], argv[2])
    elif (len(argv) == 4):
        db.add_todo(argv[0], argv[1], argv[2], argv[3])
    elif (len(argv) == 5):
        db.add_todo(argv[0], argv[1], argv[2], argv[3], argv[4])

def cmd_delete(argv):
    db = TodoListDB()
    if (len(argv) == 1):
        db.remove_todo("id=" + argv[0])

def cmd_list():
    db = TodoListDB()
    rows = db.get_todo()
    for row in rows:
        print("{0}. {1}, {2}, {3}, {4}".format(row[0], row[1], row[2], row[3], row[4]))

def main():
    import sys

    argv = sys.argv
    if 1 < len(argv):
        if argv[1] == "--version":
            print(todolist.__version__)
        elif argv[1] == "--help":
            print(todolist.__doc__)
        elif argv[1] == "--add":
            cmd_add(argv[2:])
        elif argv[1] == "--delete":
            cmd_delete(argv[2:])
        elif argv[1] == "--list":
            cmd_list()
    else:
        main_loop()

main()