def menu(options=[]):
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

    choice = ops[a-1]
    if len(choice) == 2:
        choice[1]()
    elif len(choice) == 3:
        choice[1](*choice[2])
    elif len(choice) == 4:
        choice[1](*choice[2], **choice[3])
