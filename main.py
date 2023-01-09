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


@todos.command()
def create_todo():
    todo = None

    while True:
        todo = input("Enter your todo item: ").strip()

        if not bool(todo):
            continue
        break

    cur.execute("INSERT INTO Todos (todo_item, date) VALUES (?, ?)",
                (todo, date.today()))
    conn.commit()
    print("Todo item successfully added to your todo list.")


@todos.command()
def list_todos():
    cur.execute("SELECT * FROM Todos")
    todos = cur.fetchall()

    if len(todos) == 0:
        print("There are no available todos in your todo list. Use the create-todo command to add a todo item to your list.")
    else:
        todos_table = PrettyTable(["Date", "Todo Item"])
        todos_table.align = "l"

        for todo_item in todos:
            todos_table.add_row([todo_item[3], todo_item[1]])

        print(todos_table)


if __name__ == "__main__":
    todos()
    conn.commit()
    cur.close()
