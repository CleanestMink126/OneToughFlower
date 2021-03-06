# python setup.py build

import cx_Freeze
import os
import sys
import subprocess

# os.environ['TCL_LIBRARY'] = r'C:\Program Files\Python36\tcl\tcl8.6'
# os.environ['TK_LIBRARY'] = r'C:\Program Files\Python36\tcl\tk8.6'

PACKAGES = ['pygame', 'numpy', 'scipy']
installed_packages = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).decode('utf-8')
installed_packages = installed_packages.split('\r\n')
EXCLUDES = {pkg.split('==')[0] for pkg in installed_packages if pkg != ''}
EXCLUDES.add('tkinter')
for pkg in PACKAGES:
    if type(pkg) == str:
        EXCLUDES.remove(pkg)
    else:
        EXCLUDES.remove(pkg[1])

executables = [cx_Freeze.Executable("Game.pyw", base="Win32GUI", icon="icon.ico")]
cx_Freeze.setup(
    name="PlatformGame",
    version="1.1",
    options={"build_exe": {"packages": PACKAGES,
                           "include_files": ['images/', 'audio/', 'font/'],
                           'excludes': EXCLUDES,
                           'optimize': 2}},
    executables=executables

)
[('imgs/*.png', 'imgs'), ('imgs/lava/*.png', 'imgs/lava'), ('imgs/seed/*.png', 'imgs/seed'), ('imgs/rock/*.png', 'imgs/rock'), ('imgs/ice/*.png', 'imgs/ice'), ('imgs/carrot/*.png', 'imgs/carrot'), ('imgs/dirt/*.png', 'imgs/dirt'),
 ('imgs/flowers/*.png', 'imgs/flowers'), ('imgs/iflow/*.png', 'imgs/iflow'), ('sounds/*', 'sounds'), ('sounds/seed/*', 'sounds/seed'), ('sounds/ice/*', 'sounds/ice'), ('sounds/carrot/*', 'sounds/carrot'), ('sounds/wind/*', 'sounds/wind')],
