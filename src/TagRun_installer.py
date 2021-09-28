"""
Install all files and directories into TagRun directory in Program Files under Windows or in
user home for other os
First create the root dir, next the database and the version file.
Next download from web the program .exe file
"""
import os
from platform import system
import urllib.request


class SetUp:
    def __init__(self):
        super().__init__()

        if system() == 'Windows':
            root_dir = "C:\\Program Files\\TagRun"
        else:
            root_dir = os.path.expanduser("~")

        self.exe = root_dir + "\\TagRun.exe"
        self.path_dict = {'root_dir': root_dir,
                          'db_dir': root_dir + "\\database"}

        self.create_directories()

        self.download_exe()

    def create_directories(self):
        for directory in self.path_dict.values():
            print(directory)
            if not os.path.isdir(directory):
                os.mkdir(directory)

    def download_exe(self):
        exe_url = "https://github.com/nanni00/TagRun/blob/master/app/dist/app.exe?raw=true"
        with urllib.request.urlopen(exe_url) as url:
            with open(self.exe, 'wb') as exe:
                block_size = 8192
                while True:
                    buffer = url.read(block_size)
                    if not buffer:
                        break
                    exe.write(buffer)
            exe.close()
        url.close()
# class SetUp


def main():
    SetUp()


if __name__ == "__main__":
    main()
