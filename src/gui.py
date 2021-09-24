import os
import platform
import subprocess
import tkinter
from tkinter import Tk, Listbox, END, simpledialog as sd, messagebox as mbox, BOTH, filedialog as fd
from tkinter.ttk import Frame

from database import DbTag


# todo separate gui class and functions?
class UI(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root

        # init the db
        self.db = DbTag()

        # get a tag list from db
        self.tags = self.db.get_tags()

        # the tag currently selected
        self.current_tag = None

        # list boxes used in the gui
        self.lbx_tags = None
        self.lbx_paths = None

        # dictionary used to store the current paths
        self.dict_paths = None

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
        self.rowconfigure(2, weight=1)

        button_height = 2
        button_width = 9
        buttons_row = 2

        add_tag_button = tkinter.Button(self, text="Add Tag", padx=2, pady=5, fg="white", bg="green",
                                        height=button_height, width=button_width,
                                        command=self.on_add_tag)
        add_tag_button.grid(row=buttons_row, column=0)

        add_file_path_button = tkinter.Button(self, text="Add File", padx=2, pady=5, fg="white", bg="green",
                                              height=button_height, width=button_width,
                                              command=self.on_add_file_path)
        add_file_path_button.grid(row=buttons_row, column=1)

        add_directory_path_button = tkinter.Button(self, text="Add Directory", padx=2, pady=5, fg="white", bg="green",
                                                   height=button_height, width=button_width,
                                                   command=self.on_add_dir_path)
        add_directory_path_button.grid(row=buttons_row, column=2)

        delete_tag_button = tkinter.Button(self, text="Delete Tag", padx=2, pady=5, fg="white", bg="green",
                                           height=button_height, width=button_width,
                                           command=self.on_delete_tag)
        delete_tag_button.grid(row=buttons_row, column=4)

        delete_path_button = tkinter.Button(self, text="Delete File\nor Directory", padx=2, pady=5, fg="white",
                                            bg="green", height=button_height, width=button_width,
                                            command=self.on_delete_path)
        delete_path_button.grid(row=buttons_row, column=3)

        lbx_tags = Listbox(self)
        for i in self.tags:
            lbx_tags.insert(END, i)

        lbx_tags.bind("<<ListboxSelect>>", self.on_select_tag)
        lbx_tags.grid(row=0, column=0, columnspan=5, padx=5)
        self.lbx_tags = lbx_tags

        self.lbx_paths = Listbox(self, width=50)
        self.lbx_paths.bind("<Double-Button>", self.on_select_path)
        self.lbx_paths.grid(row=1, column=0, columnspan=5)

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

    # todo handle paths dictionary on adding path to current tag
    def add_path(self, file, directory):
        if not self.db.get_tags():
            mbox.showerror(title="No Tags found", message="Add a tag before adding a path", parent=self)
        else:
            tag_name = sd.askstring("Tag", "Insert an existing tag: ", parent=self)
            if not tag_name:
                return

            path = None
            if file and not directory:
                path = fd.askopenfile(title="Choose file", initialdir=os.path.expanduser("~")).name
                # path.replace('//', '')
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
        if not idx:
            return
        self.current_tag = str(sender.get(idx))
        paths = self.db.get_paths_tagged(self.current_tag)
        self.dict_paths = self.get_paths_lbx_dict(paths)
        self.lbx_paths.delete(0, self.lbx_paths.size())

        for path in self.dict_paths.keys():
            self.lbx_paths.insert(END, path)

    def on_select_path(self, val):
        sender = val.widget
        idx = sender.curselection()
        selected_path = self.dict_paths[sender.get(idx)][0]
        if platform.system() == 'Windows':
            # print("Windows!")
            os.startfile(selected_path)
        elif platform.system() == 'Darwin':
            # print('MacOs!')
            subprocess.call(('open', selected_path))

    def on_delete_tag(self):
        if not self.db.get_tags():
            mbox.showerror(message="No tag found.")
            return

        tag_deleted = sd.askstring("Delete Tag", "Insert tag to delete: ", parent=self)
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
            mbox.showerror(message="No path found.")
            return

        tag = sd.askstring("Delete Path", "Insert path's relative tag", parent=self)
        if tag:
            if self.db.exists_tag(tag):
                path_deleted = sd.askstring("Delete Path", "Insert path to delete", parent=self)
                if self.db.exists_path_tagged(tag, path_deleted):
                    self.db.delete_path_tagged(tag, path_deleted)
                    self.lbx_paths.delete(0, self.lbx_paths.size())
                    if self.current_tag == tag:
                        for path in self.db.get_paths_tagged(tag):
                            self.lbx_paths.insert(END, path)
                    return
                mbox.showerror(message="Impossible find path '" + path_deleted + "' under tag '" + tag + "'.")
                return
            mbox.showerror(message="Impossible find tag '" + tag + "'.")
            return

    # todo use a global variable to close the app (the db) in a safe state
    def on_closing(self):
        self.db.close_connection()
        self.root.destroy()

    # todo improve relative paths building
    def get_paths_lbx_dict(self, paths):
        rel_paths = {}
        for path in paths:
            rel_path = path[0].split('/')
            rel_path.reverse()
            if not rel_paths.keys().__contains__(rel_path[0]):
                rel_paths[rel_path[0]] = path
            else:
                old_rel_path =  rel_paths.get(rel_path[0])
                old_rel_path = old_rel_path[0].split('/')
                old_rel_path.reverse()
                rel_paths[old_rel_path[1] + '/' + old_rel_path[0]] = rel_paths.pop(rel_path[0])
                rel_paths[rel_path[1] + '/' + rel_path[0]] = path

        return rel_paths


def main():
    root = Tk()
    root.geometry("400x400+300+200")

    ui = UI(root)
    root.protocol("WM_DELETE_WINDOW", ui.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
