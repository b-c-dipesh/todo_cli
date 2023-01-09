import sqlite3
from datetime import date
from prettytable import PrettyTable
from click_shell import shell

conn = sqlite3.connect('todos.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Todos (
"id" INTEGER NOT NULL UNIQUE,
"todo_item" TEXT NOT NULL UNIQUE,
"is_completed" NUMERIC NOT NULL DEFAULT 0,
"date" TEXT NOT NULL,
PRIMARY KEY ("id" AUTOINCREMENT))''')


@shell(prompt="Todos > ", intro='''Welcome to Todos App. Please enter a command down below. If you want to see a list of all available commands, enter "help".''')
def todos():
    pass


@todos.command()
def help():
    help_table = PrettyTable(["Command", "Description"])
    help_table.align = "l"

    help_table.add_row(["help", "See this table of commands."])
    help_table.add_row(
        ["list-todos", "List all the available todos from your todo list."])
    help_table.add_row(["update-todo", "Update a todo item."])
    help_table.add_row(
        ["delete-todo", "Use this to delete a todo item when you've completed it."])

    print(help_table)


if __name__ == "__main__":
    todos()
    conn.commit()
    cur.close()
