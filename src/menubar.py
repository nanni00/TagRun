from tkinter import Menu

from src.settings import Settings


class MenuBar(Menu):
    def __init__(self, root):
        Menu.__init__(self, root)

        file = Menu(self, tearoff=False)
        file.add_checkbutton(label='Show Absolute path', onvalue=1, offvalue=0, variable=Settings.SHOW_ABSOLUTE_PATH,
                             command=self.set_show_abs_path)
        self.add_cascade(label="File", menu=file)

    def set_show_abs_path(self):
        Settings.SHOW_ABSOLUTE_PATH = not Settings.SHOW_ABSOLUTE_PATH
