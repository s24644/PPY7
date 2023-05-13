import tkinter as tk
import mysql.connector

from screeninfo import get_monitors
from tkinter import ttk

root = tk.Tk()
root.title("Book Store")
root.iconbitmap("./bookshelf.ico")

def fetch_data():
    mydb = mysql.connector.connect(host="db4free.net", user="s24644", password="haslo1234", database="ppydatabase")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM books")
    result = mycursor.fetchall() # pobiera wszystkie wyniki
    mycursor.close() # Zamknięcie kursoramy
    mydb.close() # Zamknięcie połączeniareturn result
    return result


treeview = ttk.Treeview(root)

treeview["columns"] = ("id", "title", "author", "price", "category")
treeview.column("#0", width=0)
treeview.heading("id", text="ID")
treeview.heading("title", text="Tytuł")
treeview.heading("author", text="Autor")
treeview.heading("price", text="Cena")
treeview.heading("category", text="Kategoria")
treeview.pack()


def load_data():
    data = fetch_data()
    treeview.delete(*treeview.get_children())
    for row in data:
        treeview.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))


load_data()
root.mainloop()
print(fetch_data())
