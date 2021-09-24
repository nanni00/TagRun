import winreg as reg
import os
import platform
from database import DbTag
from gui import GUI


class ProgramManager:
    def __init__(self):
        super(ProgramManager, self).__init__()
        if platform.system() == 'Windows':
            root_dir = "C:\\Program Files\\TagRun"
        else:
            root_dir = os.path.expanduser("~")

        self.path_dict = {'root_dir': root_dir,
                          'db_dir': root_dir + "\\database",
                          'db_file_sqlite': root_dir + "\\database" + "\\tagrun_db.sqlite",
                          'version_file': root_dir + "\\version.txt"}

        self.db = DbTag(self.path_dict)

        with open(self.path_dict['version_file'], 'r') as v:
            self.version = float(v.read())

        if self.check_update():
            self.update()

        self.gui = GUI(self.db)
    # init()

    def remove_program(self):
        """
        Destroy the key previously created in the key_maker.py script
        You can do it manually using the Registry Editor (regedit)
        """
        key_val_command = r'Directory\\Background\\shell\\TagRun\\command'
        reg.DeleteKey(reg.HKEY_CLASSES_ROOT, key_val_command)

        key_val = r'Directory\\Background\\shell\\TagRun'
        reg.DeleteKey(reg.HKEY_CLASSES_ROOT, key_val)
    # remove_program()

    def check_update(self):
        pass

    def update(self):
        pass


def main():
    ProgramManager()


if __name__ == "__main__":
    main()
