import sys, os
_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
sys.path.insert(0, os.path.join(_root, 'Lib', 'site-packages'))
sys.path.insert(0, _root)
# from misc_codes.equipment_settings import *
# from misc_codes.general_settings import *
from powi.equipment import LecroyScope, path_maker
import getpass
username = getpass.getuser().lower()
project="DER-1015"
waveforms_folder = f'C:/Users/{username}/Desktop/{project}/'
path = path_maker(f'{waveforms_folder}')
lscope = LecroyScope("169.254.94.235")
print(path)
lscope.get_screenshot("hi.png", path)
