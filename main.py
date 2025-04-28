#Project on Library Management System
#--------------------------------------------------------------------------------
#MODULE : LIBRARY MANAGEMENT

import tkinter as tk
from tkinter import messagebox
import redis
import time
from rediStuff import search_by
from const import BOOK_RECORD_TABLE


def _does_bno_exist(r, bno):
    table_key = f"{BOOK_RECORD_TABLE}:{bno}"

    if r.exists(table_key):
        return True
    
    return False

# --- Function to search books ---
def search_books():
    bno = search_entry.get()
    if not bno:
        messagebox.showwarning("Input Error", "Please enter a Book Code or Name.")
        return

    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, socket_connect_timeout=30)

    table_key = f"{BOOK_RECORD_TABLE}:{bno}"
    
    if not _does_bno_exist(r, bno):
        results_text.insert(tk.END, "No matching books found.\n")
        return

    start_time = time.time()
    book = r.hgetall(table_key)
    elapsed_time = round(time.time() - start_time, 7)

    results_text.delete("1.0", tk.END)
    record_count = 0

    result = (
        f"Book Code: {bno}\nBook Name: {book['bname']}\nAuthor: {book['auth']}\n"
        f"Price: {book['price']}\nPublisher: {book['publ']}\nQuantity: {book['qty']}\nPurchased On: {book['date']}\n"
        + "="*50 + "\n"
    )
    results_text.insert(tk.END, result)
    record_count += 1

    if record_count == 0:
        results_text.insert(tk.END, "No matching books found.\n")

    summary_label.config(text=f"{record_count} book found in {elapsed_time} seconds")
    r.close()


# --- Show Search UI when "Book Management" is selected ---
def show_book_management():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Search Book by Code or Name:").pack(pady=5)
    global search_entry
    search_entry = tk.Entry(root, width=40)
    search_entry.pack(pady=5)

    tk.Button(root, text="Search", command=search_books).pack(pady=5)

    global results_text
    results_text = tk.Text(root, width=70, height=15)
    results_text.pack(pady=10)

    global summary_label
    summary_label = tk.Label(root, text="")
    summary_label.pack(pady=5)

    tk.Button(root, text="Back to Menu", command=show_main_menu).pack(pady=10)

# --- Main menu screen ---
def show_main_menu():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Library Management", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="1. Book Management", width=30, command=show_book_management).pack(pady=5)
    tk.Button(root, text="2. Members Management", width=30, command=lambda: messagebox.showinfo("Info", "Feature not implemented")).pack(pady=5)
    tk.Button(root, text="3. Issue/Return Book", width=30, command=lambda: messagebox.showinfo("Info", "Feature not implemented")).pack(pady=5)
    tk.Button(root, text="4. Exit", width=30, command=root.quit).pack(pady=5)
 
# --- Root Window ---
root = tk.Tk()
root.title("Library Management System")
root.geometry("600x500")

show_main_menu()

root.mainloop()
