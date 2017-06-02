import os, sys
import yaml
import cursesmenu, cursesmenu.items

from file_worker import FileWorker
from funcs import *

PATH_PREFIX = sys.argv[1]

if os.path.isfile(PATH_PREFIX+"config.yaml"):
    CONFIG = yaml.load(open(PATH_PREFIX+"config.yaml").read())
else:
    print("No config file found, using default values")
    CONFIG = {"fields":{"text":{"required":True},"description":{"required":True}}}

file_worker = FileWorker(CONFIG, PATH_PREFIX)

main_menu = ["\n\npajowu's Sample Organizer {}".format(PATH_PREFIX)
            ,["List files",file_worker.list_files]
            ,["Search",file_worker.search]
            ,["Fill in missing required fields",file_worker.check_fields]
            ,["Edit file",file_worker.edit_file]
            ,"\n"
            ]
while True:
    menu(main_menu)
