import tkinter
from tkinter import Tk, Listbox, END, StringVar, simpledialog as sd, messagebox as mbox, BOTH
from tkinter.ttk import Frame, Label

from src.database import DbTag


class UI(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.db = DbTag()

        self.var = StringVar()

        # get a tag list from db
        self.tags = self.db.get_tags()

        self.init_ui()

    def init_ui(self):
        """
        init the program's GUI
        """
        self.master.title("TagRun")
        self.pack(fill=BOTH, expand=True)

        # self.frame = tkinter.Frame(self.root, bg="white")
        # self.frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

        #self.label = Label(self.frame, text="Tags", textvariable=self.var)

        #Style().configure("TButton", padding=(0, 0, 0, 0), font='serif 10')

        self.columnconfigure(0, pad=5)
        self.columnconfigure(1, pad=5)
        self.columnconfigure(2, pad=5)
        self.columnconfigure(3, pad=5)

        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=5)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        add_tag_button = tkinter.Button(self, text="Add Tag", padx=2, pady=5, fg="white", bg="green",
                                        command=self.on_add_tag)
        # add_tag_button.pack()
        add_tag_button.grid(row=5, column=0)

        add_path_button = tkinter.Button(self, text="Add Path", padx=2, pady=5, fg="white", bg="green",
                                         command=self.on_add_path)
        # add_path_button.pack()
        add_path_button.grid(row=5, column=1)

        lbx = Listbox(self)
        for i in self.tags:
            lbx.insert(END, i)

        lbx.bind("<<ListboxSelect>>", self.on_select)
        lbx.grid(row=1, rowspan=3, columnspan=4, padx=5)
        # lbx.pack(pady=15)
        self.lb = lbx

        self.var = StringVar()
        self.lbl = Label(self, text="Tags", textvariable=self.var)
        self.lbl.grid(row=1, columnspan=4)
        # self.label.pack()

    def on_add_tag(self):
        new_tag = sd.askstring("New Tag", "Insert a new tag: ", parent=self)
        if self.db.exists_tag(new_tag):
            mbox.showwarning(message="Tag " + new_tag + " already exists.")
        else:
            self.db.insert_tag(new_tag)
            self.lb.insert(END, new_tag)

    def on_add_path(self):
        pass

    def on_select(self, val):
        sender = val.widget
        idx = sender.curselection()
        print(sender.get(idx)[0])
        paths = [j for i, j in self.db.get_paths_tagged(str(sender.get(idx)[0]))]
        print(paths)
        self.var.set(paths)


def main():
    root = Tk()
    # canvas = tkinter.Canvas(root, width=500, height=500, bg="#256D33")
    # canvas.pack()

    root.geometry("350x300+300+300")

    UI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
