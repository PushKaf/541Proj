#Project on Library Management System
#--------------------------------------------------------------------------------
#MODULE : LIBRARY MANAGEMENT
from tkinter import simpledialog
import tkinter as tk
from tkinter import messagebox
import redis
import time
from rediStuff import search_by
from const import BOOK_RECORD_TABLE
from datetime import date
from flask import Flask, request, jsonify, render_template

from const import REDIS_HOST, REDIS_PORT, ISSUE_TABLE
from rediStuff import search_by


app = Flask(__name__)

# Redis configuration (Update with your actual host and port)
REDIS_HOST = "localhost"
REDIS_PORT = 6379
client = redis.Redis(REDIS_HOST, REDIS_PORT, db=0, decode_responses=True)
def open_issue_return_window():
    issue_window = tk.Toplevel()
    issue_window.title("Issue/Return Book Management")
    issue_window.geometry("450x350")
    issue_window.configure(bg="#0056b3")

    tk.Label(
        issue_window,
        text="📚 Issue/Return Management",
        font=("Lucida Console", 18, "bold"),
        bg="#0056b3",
        fg="white"
    ).pack(pady=(30, 20))

    tk.Button(
        issue_window,
        text="➕ Issue Book",
        width=25,
        height=2,
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#0056b3",
        activebackground="#e6e6e6",
        activeforeground="#0056b3",
        relief="raised",
        bd=3,
        cursor="hand2",
        command=issue_book_ui
    ).pack(pady=10)

    tk.Button(
        issue_window,
        text="✅ Return Book",
        width=25,
        height=2,
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#0056b3",
        activebackground="#e6e6e6",
        activeforeground="#0056b3",
        relief="raised",
        bd=3,
        cursor="hand2",
        command=return_book_ui
    ).pack(pady=10)

    tk.Button(
        issue_window,
        text="🔎 Search Issued Books",
        width=25,
        height=2,
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#0056b3",
        activebackground="#e6e6e6",
        activeforeground="#0056b3",
        relief="raised",
        bd=3,
        cursor="hand2",
        command=lambda: SearchIssuedBooks(client)
    ).pack(pady=10)

def issue_book_ui():
    def submit_issue():
        r = redis.Redis(REDIS_HOST, REDIS_PORT, db=0, decode_responses=True)

        bno = entry_bno.get()
        mno = entry_mno.get()
        dd = entry_dd.get()
        mm = entry_mm.get()
        yy = entry_yy.get()

        table_key = f"{ISSUE_TABLE}:{bno}"

        if r.exists(table_key):
            messagebox.showerror("Error", "This book is already issued.")
            r.close()
            return

        issue_map = {
            "mno": mno,
            "d_o_issue": f"{dd}/{mm}/{yy}",
            "d_o_ret": ""
        }

        r.hset(table_key, mapping=issue_map)
        messagebox.showinfo("Success", f"Book {bno} issued successfully!")
        r.close()
        issue_form.destroy()

    issue_form = tk.Toplevel()
    issue_form.title("Issue a Book")
    issue_form.geometry("400x450")
    issue_form.configure(bg="#0056b3")

    tk.Label(
        issue_form,
        text="➕ Issue a Book",
        font=("Lucida Console", 16, "bold"),
        bg="#0056b3",
        fg="white"
    ).pack(pady=(30, 20))

    # Frame for inputs
    form_frame = tk.Frame(issue_form, bg="#0056b3")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Book Code:", font=("Arial", 12), bg="#0056b3", fg="white").pack(pady=5)
    entry_bno = tk.Entry(form_frame, width=30, font=("Arial", 12))
    entry_bno.pack()

    tk.Label(form_frame, text="Member Code:", font=("Arial", 12), bg="#0056b3", fg="white").pack(pady=5)
    entry_mno = tk.Entry(form_frame, width=30, font=("Arial", 12))
    entry_mno.pack()

    tk.Label(form_frame, text="Issue Date (DD/MM/YYYY):", font=("Arial", 12), bg="#0056b3", fg="white").pack(pady=5)
    frame_date = tk.Frame(form_frame, bg="#0056b3")
    frame_date.pack(pady=5)

    entry_dd = tk.Entry(frame_date, width=5, font=("Arial", 12))
    entry_mm = tk.Entry(frame_date, width=5, font=("Arial", 12))
    entry_yy = tk.Entry(frame_date, width=7, font=("Arial", 12))

    entry_dd.pack(side="left", padx=2)
    entry_mm.pack(side="left", padx=2)
    entry_yy.pack(side="left", padx=2)

    tk.Button(
        issue_form,
        text="Submit",
        width=20,
        height=2,
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#0056b3",
        activebackground="#e6e6e6",
        activeforeground="#0056b3",
        relief="raised",
        bd=3,
        cursor="hand2",
        command=submit_issue
    ).pack(pady=30)

def return_book_ui():
    def submit_return():
        r = redis.Redis(REDIS_HOST, REDIS_PORT, db=0, decode_responses=True)

        bno = entry_bno.get()
        mno = entry_mno.get()

        table_key = f"{ISSUE_TABLE}:{bno}"

        if not r.exists(table_key):
            messagebox.showerror("Error", "This book was not issued!")
            r.close()
            return

        retDate = date.today().strftime("%d/%m/%Y")
        r.hset(table_key, "d_o_ret", retDate)

        messagebox.showinfo("Success", f"Book {bno} returned successfully by Member {mno}!")
        r.close()
        return_form.destroy()

    return_form = tk.Toplevel()
    return_form.title("Return a Book")
    return_form.geometry("400x350")
    return_form.configure(bg="#0056b3")

    tk.Label(
        return_form,
        text="✅ Return a Book",
        font=("Lucida Console", 16, "bold"),
        bg="#0056b3",
        fg="white"
    ).pack(pady=(30, 20))

    form_frame = tk.Frame(return_form, bg="#0056b3")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Book Code:", font=("Arial", 12), bg="#0056b3", fg="white").pack(pady=5)
    entry_bno = tk.Entry(form_frame, width=30, font=("Arial", 12))
    entry_bno.pack()

    tk.Label(form_frame, text="Member Code:", font=("Arial", 12), bg="#0056b3", fg="white").pack(pady=5)
    entry_mno = tk.Entry(form_frame, width=30, font=("Arial", 12))
    entry_mno.pack()

    tk.Button(
        return_form,
        text="Submit",
        width=20,
        height=2,
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#0056b3",
        activebackground="#e6e6e6",
        activeforeground="#0056b3",
        relief="raised",
        bd=3,
        cursor="hand2",
        command=submit_return
    ).pack(pady=30)
    # Connect to Redis
    r = redis.Redis(REDIS_HOST, REDIS_PORT, db=0, decode_responses=True)

    # Get BNO from query parameters
    bno = request.args.get('bno')

    if not bno:
        return jsonify({"error": "Book number (BNO) is required"}), 400

    table_key = f"{BOOK_RECORD_TABLE}:{bno}"

    if not _does_bno_exist(r, bno):
        return jsonify({"error": f"BNO: {bno} doesn't exist in the table. Please add if needed."}), 404

    book = r.hgetall(table_key)

    # Prepare the response
    response = {
        "book_code": bno,
        "book_name": book.get("bname"),
        "author": book.get("auth"),
        "price": book.get("price"),
        "publisher": book.get("publ"),
        "total_quantity": book.get("qty"),
        "purchased_on": book.get("date")
    }

    r.close()

    return jsonify(response)

def SearchIssuedBooks(client):
    
    r = redis.Redis(REDIS_HOST, REDIS_PORT, db=0, decode_responses=True)

    # Prompt the user to enter Member No
    root = tk.Tk()
    root.withdraw() 
    mno = simpledialog.askstring("Search Issued Books", "Enter Member No to search issued book:")
    
    if not mno:
        messagebox.showinfo("Search Cancelled", "No Member No entered.")
        return

    res = search_by(client, mno, search_type="mno")
    Rec_count = 0

    if res.total > 0:
        output_text = ""
        for issue in res.docs:
            data = issue.__dict__
            bno = issue.id.split(":")[-1]

            Rec_count += 1
            output_text += "=============================================================\n"
            output_text += f"1. Book Code : {bno}\n"
            output_text += f"2. Member Code : {data['mno']}\n"
            output_text += f"3. Date of Issue : {data['d_o_issue']}\n"
            output_text += f"4. Date of Return : {data['d_o_ret']}\n"
            output_text += "=============================================================\n"

        # Show results in a new popup window
        result_window = tk.Toplevel()
        result_window.title(f"{Rec_count} Record(s) Found")

        text_widget = tk.Text(result_window, wrap="word", width=80, height=30)
        text_widget.insert(tk.END, output_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(padx=10, pady=10)

        # Add a button to close
        close_btn = tk.Button(result_window, text="Close", command=result_window.destroy)
        close_btn.pack(pady=5)

    else:
        messagebox.showinfo("No Records", f"No records for Member No: {mno} found.")

    r.close()
    return render_template('search_form.html')

    search_form = tk.Toplevel()
    search_form.title("Search Issued Books")

    tk.Label(search_form, text="Member Code:").pack()
    entry_mno = tk.Entry(search_form)
    entry_mno.pack()

    tk.Button(search_form, text="Search", command=search_books).pack(pady=10)

    result_text = tk.Text(search_form, height=10, width=50)
    result_text.pack()


def open_member_management():
    # Create new window
    member_window = tk.Toplevel()
    member_window.title("Member Management")
    member_window.geometry("450x450")
    member_window.configure(bg="#0056b3")  # Darker blue background

    # Title Label
    tk.Label(
        member_window,
        text="👥 Manage Members",
        font=("Lucida Console", 18, "bold"),
        bg="#0056b3",
        fg="white"
    ).pack(pady=(30, 20))

    # Insert Button
    tk.Button(
        member_window,
        text="➕ Insert Member",
        width=25,
        height=2,
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#0056b3",
        activebackground="#e6e6e6",
        activeforeground="#0056b3",
        relief="raised",
        bd=3,
        cursor="hand2",
        command=insert_member_ui
    ).pack(pady=20)

def insert_member_ui():
    # New small window for inserting member
    insert_window = tk.Toplevel()
    insert_window.title("Insert Member")
    insert_window.geometry("400x550")
    insert_window.configure(bg="#0056b3")  # Darker blue background

    # Title
    tk.Label(
        insert_window,
        text="➕ Insert New Member",
        font=("Lucida Console", 16, "bold"),
        bg="#0056b3",
        fg="white"
    ).pack(pady=(30, 20))

    labels = ["Member Code", "Member Name", "Date", "Month", "Year", "Address", "Mobile No."]
    entries = {}

    for label in labels:
        # Label for each field
        tk.Label(
            insert_window,
            text=label,
            font=("Arial", 12),
            bg="#0056b3",
            fg="white"
        ).pack(pady=(5, 2))

        # Entry for each field
        entry = tk.Entry(
            insert_window,
            width=30,
            font=("Arial", 12),
            bg="white",
            fg="black",
            bd=2,
            relief="sunken"
        )
        entry.pack(pady=(0, 10))
        entries[label] = entry

    # Submit Button (optional, you can add functionality later)
    tk.Button(
        insert_window,
        text="Submit",
        width=20,
        height=2,
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#0056b3",
        activebackground="#e6e6e6",
        activeforeground="#0056b3",
        relief="raised",
        bd=3,
        cursor="hand2"
    ).pack(pady=30)


def _does_bno_exist(r, bno):
    table_key = f"{BOOK_RECORD_TABLE}:{bno}"

    if r.exists(table_key):
        return True
    
    return False

def search_books():
    bno = search_entry.get()
    if not bno:
        messagebox.showwarning("Input Error", "Please enter a Book Code or Name.")
        return

    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True, socket_connect_timeout=30)

    table_key = f"{BOOK_RECORD_TABLE}:{bno}"

    if not _does_bno_exist(r, bno):
        results_text.insert(tk.END, "No matching books found.\n")
        summary_label.config(text="0 books found in 0 seconds")
        r.close()  
        return

    start_time = time.time()
    book = r.hgetall(table_key)
    elapsed_time = round(time.time() - start_time, 7)

    results_text.delete("1.0", tk.END)
    record_count = 0

    if book:
        result = (
            f"Book Code: {bno}\nBook Name: {book.get('bname', 'N/A')}\nAuthor: {book.get('auth', 'N/A')}\n"
            f"Price: {book.get('price', 'N/A')}\nPublisher: {book.get('publ', 'N/A')}\n"
            f"Quantity: {book.get('qty', 'N/A')}\nPurchased On: {book.get('date', 'N/A')}\n"
            + "="*50 + "\n"
        )
        results_text.insert(tk.END, result)
        record_count += 1

    if record_count == 0:
        results_text.insert(tk.END, "No matching books found.\n")

    # Update the UI summary with the count of records and time taken
    summary_label.config(text=f"{record_count} book found in {elapsed_time} seconds")
    r.close()  # Close Redis connection


def show_book_management():
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#0056b3")  # Darker fancy blue

    title_label = tk.Label(
        root, 
        text="🔎 Search Book by Code or Name:",
        font=("Lucida Console", 14, "bold"),
        bg="#0056b3",   
        fg="white"       
    )
    title_label.pack(pady=(30, 15))

    global search_entry
    search_entry = tk.Entry(root, width=40, font=("Arial", 12), bg="white", fg="black")
    search_entry.pack(pady=10)

    search_button = tk.Button(
        root, 
        text="Search", 
        width=20,
        bg="white",       
        fg="#0056b3",        
        font=("Arial", 12, "bold"),
        command=search_books,
        activebackground="#e6e6e6",
        activeforeground="#0056b3",
        relief="raised",
        bd=3,
        cursor="hand2"
    )
    search_button.pack(pady=10)

    global results_text
    results_text = tk.Text(
        root, 
        width=70, 
        height=15, 
        font=("Courier", 11),
        bg="white",
        fg="black"
    )
    results_text.pack(pady=20)

    global summary_label
    summary_label = tk.Label(root, text="0 books found in 0 seconds", font=("Arial", 10), bg="#0056b3", fg="white")
    summary_label.pack(pady=10)

    back_button = tk.Button(
        root, 
        text="⬅️ Back to Menu", 
        width=20,
        bg="white",
        fg="#0056b3",
        font=("Arial", 12, "bold"),
        command=show_main_menu,
        activebackground="#e6e6e6",
        activeforeground="#0056b3",
        relief="raised",
        bd=3,
        cursor="hand2"
    )
    back_button.pack(pady=(30, 30))

def show_main_menu():
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#0056b3")

    # Title
    title_label = tk.Label(
        root, 
        text="Library Management System",
        font=("Lucida Console", 22, "bold"),
        bg="#0056b3",
        fg="white"
    )
    title_label.pack(pady=(40, 30))

    # Styled button easily
    def create_menu_button(text, command):
        return tk.Button(
            root,
            text=text,
            width=30,
            height=2,
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#0056b3",              
            activebackground="#e6e6e6",
            activeforeground="#0056b3",
            relief="raised",
            bd=3,
            command=command,
            cursor="hand2"            
        )

    # Buttons
    create_menu_button("📚  1. Book Management", show_book_management).pack(pady=12)
    create_menu_button("👤  2. Members Management", open_member_management).pack(pady=12)
    create_menu_button("🔄  3. Issue/Return Book", open_issue_return_window).pack(pady=12)
    create_menu_button("🚪  4. Exit", root.quit).pack(pady=(30, 30))


# --- Root Window ---
root = tk.Tk()
root.title("Library Management System")
root.geometry("600x500")

show_main_menu()

root.mainloop()