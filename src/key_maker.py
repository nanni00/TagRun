"""
The script creates keys context menu. Credits to :seddie95 (https://github.com/seddie95)
"""

import winreg as reg
import os
import sys

cwd = os.getcwd()
python_exe = sys.executable

# hide terminal
hidden_terminal = '\\'.join(python_exe.split('\\')[:-1])+"\\pythonw.exe"

# path of the context menu option
key_val = r'Directory\\Background\\shell'

# Create first key which will display the name in the context menu
key2change = reg.OpenKey(reg.HKEY_CLASSES_ROOT, key_val, 0, reg.KEY_ALL_ACCESS)
key = reg.CreateKey(key2change, r"TagRun\\")
reg.SetValue(key, '', reg.REG_SZ, '&TagRun here')
reg.CloseKey(key)

# Create 2nd key which will run the python script
key2change1 = reg.OpenKey(reg.HKEY_CLASSES_ROOT, key_val, 0, reg.KEY_ALL_ACCESS)
key1 = reg.CreateKey(key2change1, r"TagRun\\command")
reg.SetValue(key1, '', reg.REG_SZ, python_exe + f' "{cwd}\\program_manager.py"')
reg.SetValue(key1, '', reg.REG_SZ, hidden_terminal + f' "{cwd}\\program_manager.py"')  # use to to hide terminal
reg.CloseKey(key1)
