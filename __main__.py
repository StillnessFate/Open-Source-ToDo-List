from todolistdb import TodoListDB

db = TodoListDB()
db.add_category("생활")
db.add_category("개발")

columns = ("id", "할일", "기한", "카테고리", "완료")

def main_menu():
    while True:
        print("Choose an option.")
        ans = input(" 1. Add todo\n 2. List todo\n 3. Modify todo\n 4. Quit\n\n >>> ")

        if ans == "1":
            # Add todo
            add_todo()
        
        elif ans == "2":
            # List todo
            list_todo()
        
        elif ans == "3":
            # Modify todo
            modify_todo()
        
        elif ans == "4":
            # Quit
            break
        else:
            print("Please select a proper option.\n")

########## Main menu functions ##########

def add_todo():
    # Add todo list
    a = input("Todo : ")
    b = input("Due date : ")
    print("Choose a category")
    list_category()
    cat = input(" >>> ") # This line needs to be fixed. (#1) safety coding
    db.add_todo(a, b, cat)

def list_todo():
    # List todo list
    while True:
        print("Choose a listing option.\n")
        ans = input(" 1. Just list them all\n 2. Category options\n 3. Back to main menu\n\n >>> ")

        if ans == "1":
            # List them all
            list_all()

        elif ans == "2":
            # Category options
            while True:
                print("\n###Category options###")
                opt = input(" 1. Add new category\n 2. Delete category\n 3. List category\n 4. Back to listing options\n\n>>> ")

                if opt == "1":
                    # Add new category
                    add_category()
                
                elif opt == "2":
                    # Delete category
                    del_category()

                elif opt == "3":
                    # List category
                    list_category()
                
                elif opt == "4":
                    # Go back to previous menu
                    break
                
                else:
                    print("Please select a proper option.\n")

        elif ans == "3":
            # Back to main menu
            break

        else:
            print("Please choose a proper option.\n")

def modify_todo():
    # Modify todo list
    while True:
        print("Modify options")
        ans = input(" 1. Modify contents\n 2. Mark as finished/not finished\n 3. Delete todo\n 4. Back to previous menu\n\n >>> ")

        if ans == "1":
            # Modify contents
            modify_contents()
        
        elif ans == "2":
            # Mark as finished/not finished
            finished()
        
        elif ans == "3":
            # Delete todo
            delete_todo()

        elif ans == "4":
            # Back to previous menu
            break
        
        else:
            print("Please select a proper option.\n")

def list_all():
    # List all To-dos here
    columns = ("id", "할일", "기한", "카테고리", "완료")
    todo = db.get_todo()
    print_table(columns, todo, 10)

########################################

########## Category functions ##########

def add_category():
    # Add a category
    category = input("Please input category name here : ")
    db.add_category(category)

    # This needs to be safely coded.

def del_category():
    # Delete a category
    list_category()
    print("Input category id that you want to delete.")
    rec_id = input(" >>> ")
    while True:
        ans = input("Are you sure ? (Y/N) : ")
        if ans == "y" or ans == "Y":
            db.remove_category("id=" + rec_id)
            print("Deleted.")
            break
        elif ans == "n" or ans == "N":
            print("Aborted!")
            break
        else:
            pass

def list_category():
    # List existing categories
    # Additional changes could be made here. (ex:Print pretty)
    columns = ("ID","카테고리")
    todo = db.get_row("category")
    print_table(columns, todo, 10)

########################################

########## Modifing option functions ##########

def modify_contents():
    # Modify contents
    list_all()
    rec_id = input("Input record id : ")
    if rec_id.isdigit():
        print("You can just press ENTER if you want to skip certain item.")
        what = input("Input todo : ")
        due = input("Input due : ")
        cat = input("Input category : ")
        
        if what == "" and (due != "" and cat != ""): # a b' c'
            modifys = (("due", due), ("category", cat))
            db.modify_todo(modifys, "id=" + rec_id)

        elif due == "" and (what != "" and cat != ""): # b a' c'
            modifys = (("what", what), ("category", cat))
            db.modify_todo(modifys, "id=" + rec_id)

        elif cat == "" and (what != "" and due != ""): # c a' b'
            modifys = (("what", what), ("due", due))
            db.modify_todo(modifys, "id=" + rec_id)

        elif what != "" and (due == "" and cat == ""): # a' b c
            modifys = (("what", what),)
            db.modify_todo(modifys, "id=" + rec_id)

        elif due != "" and (what == "" and cat == ""): # b' a c
            modifys = (("due", due),)
            db.modify_todo(modifys, "id=" + rec_id)

        elif cat != "" and (what == "" and due == ""): # c' a b
            modifys = (("category", cat),)
            db.modify_todo(modifys, "id=" + rec_id)

        elif what != "" and due != "" and cat != "": # a' b' c'
            modifys = (("what", what), ("due", due), ("category", cat))
            db.modify_todo(modifys, "id=" + rec_id)

        else: # a b c
            print("You have to fill in something...")
            
    else:
        print("Please input a proper record id.\n")
        # Additional safety coding needed.

def finished():
    # Mark as finished or not finished
    print("Input record id that you want to mark as finished/not finished.")
    list_all()
    rec_id = input("Record id : ")
    print("1. Finished\n2. Not finished\n")
    ans = input(" >>> ")
    if ans == "1":
        modifys = (("finished", "1"),)
        db.modify_todo(modifys, "id = " + rec_id)

    elif ans == "2":
        modifys = (("finished", "0"),)
        db.modify_todo(modifys, "id = " + rec_id)

    else:
        print("Please select a proper option.\n")

def delete_todo():
    # Delete a certain todo list
    print("Input record id that you want to delete")
    list_all()
    rec_id = input("Record id : ")
    while True:
        ans = input("Are you sure ? (Y/N) : ")
        if ans == "y" or ans == "Y":
            db.remove_todo("id=" + rec_id)
            print("Deleted.")
            break
        elif ans == "n" or ans == "N":
            print("Aborted!")
            break
        else:
            pass


###############################################

########## Print functions ##########

def print_table(columns, rows, min_width=10):
    valid_columns = []
    for idx, column in enumerate(columns):
        if column:
            valid_columns.append({
                "idx": idx,
                "print_width": get_print_width(column)
            })

    if not valid_columns:
        return

    for row in rows:
        for vcolumn in valid_columns:
            print_width = get_print_width(row[vcolumn["idx"]])
            if (vcolumn["print_width"][0] < print_width[0]):
                vcolumn["print_width"] = print_width

    print("┌", end="")
    for vcolumn in valid_columns:
        print("─" * max(vcolumn["print_width"][0] + 1, min_width), end="")
        if valid_columns[-1] is not vcolumn:
            print("┬", end="")
    print("┐")

    for vcolumn in valid_columns:
        text = columns[vcolumn["idx"]]
        print_width = get_print_width(text)
        format_base = "│{0:>" + \
            str(max(vcolumn["print_width"][0] + 1,
                    min_width) - print_width[2]) + "}"
        print(format_base.format(text), end="")
    print("│")

    print("├", end="")
    for vcolumn in valid_columns:
        print("─" * max(vcolumn["print_width"][0] + 1, min_width), end="")
        if valid_columns[-1] is not vcolumn:
            print("┼", end="")
    print("┤")

    for row in rows:
        for vcolumn in valid_columns:
            text = row[vcolumn["idx"]]
            print_width = get_print_width(text)
            format_base = "│{0:>" + \
                str(max(vcolumn["print_width"][0] + 1,
                        min_width) - print_width[2]) + "}"
            print(format_base.format(text), end="")
        print("│")

    print("└", end="")
    for vcolumn in valid_columns:
        print("─" * max(vcolumn["print_width"][0] + 1, min_width), end="")
        if valid_columns[-1] is not vcolumn:
            print("┴", end="")
    print("┘")

def get_print_width(s):
    s = str(s)
    print_width = 0
    len = 0
    wide_num = 0

    for c in s:
        c_ord = ord(c)
        if (
            (ord('A') <= c_ord <= ord('Z')) or
            (ord('a') <= c_ord <= ord('z')) or
            (ord('0') <= c_ord <= ord('9')) or
            (c in " !?()_-+=@#$%^&*\\/<>,.")
        ):
            print_width += 1
        elif (
            (ord('ㄱ') <= c_ord <= ord('ㅣ')) or
            (ord('가') <= c_ord <= ord('ퟻ'))
        ):
            print_width += 2
            wide_num += 1
        else:
            return None
        len += 1

    return (print_width, len, wide_num)

#####################################

main_menu()
