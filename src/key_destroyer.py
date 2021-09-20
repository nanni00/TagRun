import winreg as reg

"""
Destroy the key previously created in the key_maker.py script
You can do it manually using the Registry Editor (regedit)
"""

key_val_command = r'Directory\\Background\\shell\\TagRun\\command'
reg.DeleteKey(reg.HKEY_CLASSES_ROOT, key_val_command)

key_val = r'Directory\\Background\\shell\\TagRun'
reg.DeleteKey(reg.HKEY_CLASSES_ROOT, key_val)
