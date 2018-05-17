import sqlite3

todo_list_table_name = "todo_list"

todo_list_columns = [
    ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
    ("what", "TEXT NOT NULL"),
    ("due", "TEXT NOT NULL"),
    ("category", "TEXT NOT NULL"),
    ("finished", "INTEGER NOT NULL")
]

class TodoListDB():

    def __init__(self, file="todolist.db"):
        self.conn = sqlite3.connect(file)
        self.cur = self.conn.cursor()

        self.create_table(todo_list_table_name, todo_list_columns)

    # TODO ==============================
    def add_todo(self, what, due, category):
        query = (
            "INSERT INTO {0} (what, due, category, finished) VALUES"
            "('{1}', '{2}', '{3}', '{4}');"
        ).format(
            todo_list_table_name,
            what,
            due,
            category,
            0
        )

        self.cur.execute(query)
        self.conn.commit()

    def remove_todo(self, where_exp):
        self.remove_row(todo_list_table_name, where_exp)

    def modify_todo(self, modifys, where_exp):
        self.modify_row(todo_list_table_name, modifys, where_exp)

    def get_todo(self, where_exp="1"):
        return self.get_row(todo_list_table_name, where_exp)

    # DB(don't care) ==============================
    def create_table(self, name, columns):
        query = ("CREATE TABLE IF NOT EXISTS {0} ({1});").format(
            name,
            ",".join([(x[0] + " " + x[1]) for x in columns])
        )

        self.cur.execute(query)
        self.conn.commit()

    def get_row(self, table, where_exp="1"):
        query = ("SELECT * FROM {0} WHERE {1};").format(
            table,
            where_exp
        )

        self.cur.execute(query)
        return self.cur.fetchall()

    def remove_row(self, table, where_exp):
        query = ("DELETE FROM {0} WHERE {1};").format(
            table,
            where_exp
        )

        self.cur.execute(query)
        self.conn.commit()

    def modify_row(self, table, modifys, where_exp):
        query = ("UPDATE {0} SET {1} WHERE {2};").format(
            table,
            ",".join([(x[0] + "='" + x[1] + "'") for x in modifys]),
            where_exp
        )

        self.cur.execute(query)
        self.conn.commit()

    def is_inside_row(self, table, where_exp):
        return bool(self.get_row(table, where_exp))
