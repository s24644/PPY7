import sqlite3
import tkinter as tk
from tkinter import ttk

conn = sqlite3.connect('studenci.db')

root = tk.Tk()
root.title("Studenci")
root.iconbitmap("./bookshelf.ico")
root.geometry(f"1400x640")


def fetch_data():
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM studenci")
    result = mycursor.fetchall()  # pobiera wszystkie wyniki
    mycursor.close()  # Zamknięcie kursoramy
    # conn.close() # Zamknięcie połączeniareturn result
    return result


def load_data():
    data = fetch_data()
    treeview.delete(*treeview.get_children())
    for row in data:
        treeview.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))


def add_student():
    text_data = add_student_entry.get()
    splitted = text_data.split(",")
    query = f"INSERT INTO studenci VALUES ({int(splitted[0])}, '{splitted[1]}', '{splitted[2]}', " \
            f"{float(splitted[3])}, {int(splitted[4])})"
    conn.execute(query)
    load_data()


def delete_student():
    id_to_delete = int(delete_student_entry.get())
    query = f"DELETE FROM studenci WHERE id = {id_to_delete}"
    conn.execute(query)
    load_data()

def alter_student():
    id_to_alter = int(alter_student_entry1.get())
    text_data = alter_student_entry2.get()
    splitted_data = text_data.split(",")
    query = f"UPDATE studenci SET imie='{splitted_data[0]}', nazwisko = '{splitted_data[1]}', " \
            f"punkty = {int(splitted_data[2])}, ocena = {int(splitted_data[3])} WHERE id={id_to_alter}"
    print(query)
    conn.execute(query)
    load_data()


create_table_query = '''CREATE TABLE IF NOT EXISTS studenci (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        imie TEXT,                            
                        nazwisko TEXT,                            
                        punkty REAL,                            
                        ocena INTEGER                        
                        )'''

conn.execute(create_table_query)

left_frame = tk.Frame(root, borderwidth=4, relief="ridge", width=int(root.winfo_width() + 100),
                      height=int(root.winfo_height() * 2.5))
left_frame.pack(side="left", padx=10, pady=10)
left_frame.pack_propagate(0)

add_student_label = tk.Label(left_frame, text="Aby dodać studenta, podaj jego dane oddzielone ','")
add_student_label.pack(padx=10, pady=10)

add_student_entry = tk.Entry(left_frame)
add_student_entry.pack(anchor="n", padx=10, pady=10)

add_student_button = tk.Button(left_frame, text="Wprowadź dane", command=add_student)
add_student_button.pack(anchor="center", padx=10, pady=10)

delete_student_label = tk.Label(left_frame, text="Aby usunąć studenta, podaj jego id")
delete_student_label.pack(padx=10, pady=10)

delete_student_entry = tk.Entry(left_frame)
delete_student_entry.pack(anchor="n", padx=10, pady=10)

delete_student_button = tk.Button(left_frame, text="Usun studenta", command=delete_student)
delete_student_button.pack(anchor="center", padx=10, pady=10)

alter_student_label = tk.Label(left_frame, text="Podaj id studenta do edycji oraz jego nowe dane")
alter_student_label.pack(padx=10, pady=10)

alter_student_entry1 = tk.Entry(left_frame)
alter_student_entry1.pack(anchor="n", padx=10, pady=10)

alter_student_entry2 = tk.Entry(left_frame)
alter_student_entry2.pack(anchor="n", padx=10, pady=10)

alter_student_button = tk.Button(left_frame, text="Zmien dane studenta", command=alter_student)
alter_student_button.pack(anchor="center", padx=10, pady=10)

right_frame = tk.Frame(root, width=int(root.winfo_width() * 5), height=left_frame["height"], borderwidth=4,
                       relief="ridge")
right_frame.pack(side="right", padx=10, pady=10)
right_frame.pack_propagate(0)

treeview = ttk.Treeview(right_frame)
treeview["columns"] = ("id", "imie", "nazwisko", "punkty", "ocena")
treeview.column("#0", width=0)
treeview.heading("id", text="ID")
treeview.heading("imie", text="Imie")
treeview.heading("nazwisko", text="Nazwisko")
treeview.heading("punkty", text="Punkty")
treeview.heading("ocena", text="Ocena")
treeview.pack()

conn.execute('''INSERT INTO studenci VALUES (1, 'Jan', 'Kowalski', '66', '3.5')''')

show_data_button = tk.Button(right_frame, text="Wyświetl dane w tabeli", command=load_data)
show_data_button.pack(anchor="center", padx=10, pady=10)

# load_data()
root.mainloop()
