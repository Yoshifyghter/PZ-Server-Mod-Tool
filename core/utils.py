def menu(title,options):

    print("\n"+title)
    for i,o in enumerate(options,1):
        print(f"{i}. {o}")

    while True:
        try:
            c=int(input("> "))
            if 1<=c<=len(options):
                return c-1
        except:
            pass