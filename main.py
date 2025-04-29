# main.py
import tkinter as tk
from ui_functions import open_issue_return_window, open_member_management, search_books, show_book_management

def main():

    # Create the main root window
    root = tk.Tk()
    root.title("Library Management System")
    root.geometry("500x400")
    root.configure(bg="#0056b3")

    # Add some main buttons to open other windows
    tk.Label(
        root,
        text="📚 Library Management System",
        font=("Lucida Console", 18, "bold"),
        bg="#0056b3",
        fg="white"
    ).pack(pady=(30, 20))

    tk.Button(
        root,
        text="Manage Members",
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
        command=open_member_management
    ).pack(pady=10)

    tk.Button(
        root,
        text="Issue/Return Books",
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
        command=open_issue_return_window
    ).pack(pady=10)

    # Start the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()
