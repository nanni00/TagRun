import winreg as reg
import os
import platform
import urllib.request
from src.database import DbTag
from src.gui import GUI


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
        """
        :return: True if an update is available
        """
        if not os.path.isfile(self.path_dict['version_file']):
            with open(self.path_dict['version_file'], 'w') as f:
                f.write('1.0')
                f.close()

        url = "https://raw.githubusercontent.com/Giovanni-M00/TagRun/master/version"
        with urllib.request.urlopen(url) as vu:
            v = float(vu.read())
            print(v)
        with open(self.path_dict['version_file'], 'r') as vu1:
            current_version = float(vu1.read())

        return current_version < v

    def update(self):

        pass

