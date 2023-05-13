import sqlite3
import tkinter as tk
from tkinter import ttk

conn = sqlite3.connect('studenci.db')

root = tk.Tk()
root.title("Studenci")
root.iconbitmap("./bookshelf.ico")
root.geometry(f"1400x500")


def fetch_data():
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM studenci")
    result = mycursor.fetchall()
    mycursor.close()
    return result


def load_data():
    data = fetch_data()
    treeview.delete(*treeview.get_children())
    for row in data:
        treeview.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))


def add_student():  # Dopiero później zobaczyłem że może chodzić o otwarcie nowego okna, edycja studenta już będzie tak zrealizowana :)
    text_data = add_student_entry.get()
    splitted = text_data.split(",")
    query = f"INSERT INTO studenci VALUES ({int(splitted[0])}, '{splitted[1]}', '{splitted[2]}', " \
            f"{float(splitted[3])}, {float(splitted[4])})"
    conn.execute(query)
    load_data()


def delete_student():
    id_to_delete = int(delete_student_entry.get())
    query = f"DELETE FROM studenci WHERE id = {id_to_delete}"
    conn.execute(query)
    load_data()


def open_details_window(event):
    selected_item = treeview.focus()

    if selected_item:
        item_data = treeview.item(selected_item)
        item_values = item_data["values"]

        details_window = tk.Toplevel(root)
        details_window.title("Szczegóły")

        id_label = ttk.Label(details_window, text="ID: ")
        id_label.pack()
        id_entry = ttk.Entry(details_window)
        id_entry.insert(0, item_values[0])
        id_entry.pack()

        first_name_label = ttk.Label(details_window, text="Imie: ")
        first_name_label.pack()
        first_name_entry = ttk.Entry(details_window)
        first_name_entry.insert(0, item_values[1])
        first_name_entry.pack()

        last_name_label = ttk.Label(details_window, text="Nazwisko: ")
        last_name_label.pack()
        last_name_entry = ttk.Entry(details_window)
        last_name_entry.insert(0, item_values[2])
        last_name_entry.pack()

        points_label = ttk.Label(details_window, text="Punkty: ")
        points_label.pack()
        points_entry = ttk.Entry(details_window)
        points_entry.insert(0, item_values[3])
        points_entry.pack()

        grade_label = ttk.Label(details_window, text="Ocena: ")
        grade_label.pack()
        grade_entry = ttk.Entry(details_window)
        grade_entry.insert(0, item_values[4])
        grade_entry.pack()

        def alter_student():
            query = f"UPDATE studenci SET imie='{first_name_entry.get()}', nazwisko = '{last_name_entry.get()}', " \
                    f"punkty = {float(points_entry.get())}, ocena = {float(grade_entry.get())} WHERE id={id_entry.get()}"
            conn.execute(query)
            load_data()

        alter_button = tk.Button(details_window, text="Zmien dane studenta", command=alter_student)
        alter_button.pack()


create_table_query = '''CREATE TABLE IF NOT EXISTS studenci (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        imie TEXT,                            
                        nazwisko TEXT,                            
                        punkty REAL,                            
                        ocena REAL                        
                        )'''

conn.execute(create_table_query)

left_frame = tk.Frame(root, borderwidth=4, relief="ridge", width=int(root.winfo_width() + 100),
                      height=int(root.winfo_height() * 2))
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
treeview.bind("<Double-1>", open_details_window)

conn.execute('''INSERT INTO studenci VALUES (1, 'Jan', 'Kowalski', '66', '3.5')''')

show_data_button = tk.Button(right_frame, text="Wyświetl dane w tabeli", command=load_data)
show_data_button.pack(anchor="center", padx=10, pady=10)

alter_student_label = tk.Label(right_frame, text="Aby zmienić dane studenta, kliknij na niego podwójnie na tabeli",
                               font=("Arial", 10))
alter_student_label.pack(padx=10, pady=10)

root.mainloop()
