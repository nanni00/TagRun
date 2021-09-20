from database import DbTag
from tkinter import Tk, Frame, simpledialog as sd, messagebox as mbox


def key_add_path():
    db = DbTag()
    root = Tk()
    root.geometry("100x100+300+300")
    frame = Frame(root)
    frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
    root.withdraw()
    frame = Frame(root)
    frame.pack()

    tag = sd.askstring("Add Path", "Insert an existing tag: ", parent=root)
    if tag:
        if db.exists_tag(tag):
            path = sd.askstring("Add Path", "Insert an absolute path: ", parent=root)
            if path:
                if not db.exists_path_tagged(tag, path):
                    db.insert_path(tag, path)
                mbox.showerror("Error", "Path '" + path + "' has already been tagged with '" + tag + "'.", parent=frame)
                return
            return
        mbox.showerror("Error", "Tag '" + tag + "' not found.", parent=root)

    root.mainloop()


if __name__ == "__main__":
    key_add_path()
