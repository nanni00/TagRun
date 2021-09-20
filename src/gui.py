import os
import tkinter
from tkinter import Tk, Listbox, END, simpledialog as sd, messagebox as mbox, BOTH, filedialog as fd
from tkinter.ttk import Frame

from src.database import DbTag


class UI(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.db = DbTag()

        # self.var = StringVar()

        # get a tag list from db
        self.tags = self.db.get_tags()
        print(self.tags)

        # the tag currently selected
        self.current_tag = None

        self.init_ui()

    def init_ui(self):
        """
        init the program's GUI
        """
        self.master.title("TagRun")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(0, pad=5)
        self.columnconfigure(1, pad=5)
        self.columnconfigure(2, pad=5)
        self.columnconfigure(3, pad=5)

        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=5)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        button_height = 2
        button_width = 9

        add_tag_button = tkinter.Button(self, text="Add Tag", padx=2, pady=5, fg="white", bg="green",
                                        height=button_height, width=button_width,
                                        command=self.on_add_tag)
        add_tag_button.grid(row=5, column=0)

        add_file_path_button = tkinter.Button(self, text="Add File", padx=2, pady=5, fg="white", bg="green",
                                              height=button_height, width=button_width,
                                              command=self.on_add_file_path)
        add_file_path_button.grid(row=5, column=1)

        add_directory_path_button = tkinter.Button(self, text="Add Directory", padx=2, pady=5, fg="white", bg="green",
                                                   height=button_height, width=button_width,
                                                   command=self.on_add_dir_path)
        add_directory_path_button.grid(row=5, column=2)

        delete_tag_button = tkinter.Button(self, text="Delete Tag", padx=2, pady=5, fg="white", bg="green",
                                           height=button_height, width=button_width,
                                           command=self.on_delete_tag)
        delete_tag_button.grid(row=5, column=4)

        delete_path_button = tkinter.Button(self, text="Delete File\nor Directory", padx=2, pady=5, fg="white",
                                            bg="green", height=button_height, width=button_width,
                                            command=self.on_delete_path)
        delete_path_button.grid(row=5, column=3)

        lbx_tags = Listbox(self)
        for i in self.tags:
            lbx_tags.insert(END, i)

        lbx_tags.bind("<<ListboxSelect>>", self.on_select_tag)
        lbx_tags.grid(row=0, column=0, columnspan=5, padx=5)
        self.lbx_tags = lbx_tags

        self.lbx_paths = Listbox(self)
        self.lbx_paths.bind("<<ListboxSelect>>", self.on_select_path)
        self.lbx_paths.grid(row=1, column=0, columnspan=5, ipadx=50)

    def on_add_tag(self):
        new_tag = sd.askstring("New Tag", "Insert a new tag: ", parent=self)
        if not new_tag:
            return
        elif self.db.exists_tag(new_tag):
            mbox.showwarning(message="Tag " + new_tag + " already exists.")
        else:
            self.tags.append(new_tag)
            self.db.insert_tag(new_tag)
            self.lbx_tags.insert(END, new_tag)

    def on_add_file_path(self):
        self.add_path(file=True, directory=False)

    def on_add_dir_path(self):
        self.add_path(file=False, directory=True)

    def add_path(self, file, directory):
        if not self.db.get_tags():
            mbox.showerror(title="No Tags found", message="Add a tag before adding a path", parent=self)
        else:
            tag_name = sd.askstring("Tag", "Insert an existing tag: ", parent=self)
            if not tag_name:
                return

            path = None
            if file and not directory:
                path = fd.askopenfile('r', title="Choose file", initialdir=os.path.expanduser("~"))
            elif not file and directory:
                path = fd.askdirectory(title="Choose directory", initialdir=os.path.expanduser("~"))

            if self.db.exists_path_tagged(tag_name, str(path)):
                mbox.showerror(message="Path " + str(path) + " is already been tagged with " + tag_name + ".")
                return

            if path:
                self.db.insert_path(tag_name, str(path))
                if self.current_tag == tag_name:
                    self.lbx_paths.insert(END, path)

    def on_select_tag(self, val):
        sender = val.widget
        idx = sender.curselection()
        self.current_tag = str(sender.get(idx))
        paths = self.db.get_paths_tagged(self.current_tag)
        self.lbx_paths.delete(0, self.lbx_paths.size())

        for path in paths:
            self.lbx_paths.insert(END, path)

    def on_select_path(self, val):
        list_path = self.db.get_paths_tagged(self.current_tag)

    def on_delete_tag(self):
        tag_deleted = sd.askstring("Delete Tag", "Insert tag to destroy: ", parent=self)
        if not tag_deleted:
            return
        if not self.db.exists_tag(tag_deleted):
            mbox.showerror(message="Impossible find tag: " + tag_deleted)
        else:
            self.db.delete_tag(tag_deleted)
            self.tags.remove(tag_deleted)

            self.lbx_tags.delete(0, self.lbx_paths.size())

            for tag in self.tags:
                self.lbx_tags.insert(END, tag)

            if self.current_tag == tag_deleted:
                self.lbx_paths.delete(0, self.lbx_paths.size())

    def on_delete_path(self):
        if not self.db.get_tags():
            mbox.showerror(message="Path list is empty yet.")
            return

        frame2 = tkinter.Frame()
        frame2.place(self.root)
        # todo finish listbox on destroy path


def main():
    root = Tk()
    root.geometry("400x500+300+200")

    UI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
