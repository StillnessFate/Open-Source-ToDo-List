from todolistdb import TodoListDB


def main():
    db = TodoListDB()

    db.remove_todo("1")
    db.remove_category("1")

    db.add_category("생활")
    db.add_category("개발")

    db.add_todo("잠자기", "새벽 2시", "생활")
    db.add_todo("점심 먹기", "낮 12시", "생활")
    db.add_todo("그냥 있기", "항상")
    db.add_todo("프로그래밍 하기", "하고 싶을 때", "개발")

    columns = ("", "할일", "기한", "카테고리", "완료")

    # ------------------------------

    print("<기본>")
    todos = db.get_todo()
    print_table(columns, todos, 10)

    # ------------------------------

    db.add_todo("프로그래밍 하기", "항상", "생활")

    print("<중복 삽입 무시>")
    todos = db.get_todo()
    print_table(columns, todos, 10)

    # ------------------------------

    db.add_todo("무언가", "언젠가", "모름")

    print("<없는 카테고리 삽입 무시>")
    todos = db.get_todo()
    print_table(columns, todos, 10)

    # ------------------------------

    modifys = (("due", "가끔씩"), ("category", "생활"), ("finished", "1"))
    db.modify_todo(modifys, "what='그냥 있기'")

    print("<수정>")
    todos = db.get_todo()
    print_table(columns, todos, 10)

    # ------------------------------

    db.remove_todo("what='잠자기'")

    print("<삭제>")
    todos = db.get_todo()
    print_table(columns, todos, 10)

    # ------------------------------

    print("<필터링>")
    todos = db.get_todo("category='생활'")
    print_table(columns, todos, 10)

    # ------------------------------

    print("<최소폭 수정>")
    todos = db.get_todo()
    print_table(columns, todos, 20)

    # ------------------------------

    columns = ("id", "할일", "기한", "카테고리", "완료")

    print("<모든 컬럼>")
    todos = db.get_todo()
    print_table(columns, todos, 10)

    # ------------------------------

    columns = ("", "할일", "", "", "")

    print("<일부 컬럼>")
    todos = db.get_todo()
    print_table(columns, todos, 10)
    

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
        format_base = "│{0:>" + str(max(vcolumn["print_width"][0] + 1, min_width) - print_width[2]) + "}"
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
            format_base = "│{0:>" + str(max(vcolumn["print_width"][0] + 1, min_width) - print_width[2]) + "}"
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


# main()

# import os
# import shutil
# print(os.get_terminal_size())
# print(shutil.get_terminal_size())