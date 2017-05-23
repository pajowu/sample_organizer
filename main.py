import os, sys
import yaml
import cursesmenu, cursesmenu.items

from file_worker import FileWorker

PATH_PREFIX = sys.argv[1]

if os.path.isfile(PATH_PREFIX+"config.yaml"):
    CONFIG = yaml.load(open(PATH_PREFIX+"config.yaml").read())
    print(CONFIG)
else:
    print("No config file found, using default values")
    CONFIG = {"fields":{"text":{"required":True},"description":{"required":True}}}

file_worker = FileWorker(CONFIG, PATH_PREFIX)

def menu(options=[]):
    print("\n\n")
    ops = []
    for item in options:
        if type(item) == str:
            print(item)
        elif type(item) == list:
            ops.append(item)
            print("{}: {}".format(len(ops),item[0]))

    a = int(input("Menu choice: "))
    if 0 > a or a > len(ops):
        print("Choice out of bounds")
        menu(options=options)

    print()

    choice = ops[a-1]
    if len(choice) == 2:
        choice[1]()
    elif len(choice) == 3:
        choice[1](*choice[2])
    elif len(choice) == 4:
        choice[1](*choice[2], **choice[3])

main_menu = ["pajowu's Sample Organizer {}".format(PATH_PREFIX),["List files",file_worker.list_files],["Fill in missing required fields",file_worker.check_fields]]
while True:
    menu(main_menu)
