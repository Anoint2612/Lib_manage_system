import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
from pymongo import MongoClient

# This class implements a Library Management System with a GUI built using Tkinter.
# It provides features for managing books, users, and borrowing activities while storing data in MongoDB.


class LibraryManagementSystem:
    #this is a comit for contructor
    def _init_(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("800x900")
        self.root.configure(bg="#f0f2f5")
        
        # MongoDB setup connected to cluster
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["library_db"]
        self.books_collection = self.db["books"]
        self.users_collection = self.db["users"]
        self.borrowed_books_collection = self.db["borrowed_books"]
        
        # Configure styles
        self.setup_styles()
        
        # Create main container
        self.main_container = ttk.Frame(self.root, padding="20")
        self.main_container.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create header
        self.create_header()
        
        # Create tabbed interface
        self.create_tabs()

    def setup_styles(self):
        self.style = ttk.Style()
        
        # Configure colors
        self.style.configure(".",
            background="#f0f2f5",
            foreground="#1a1a1a",
            font=("Helvetica", 10)
        )
        
        # Header style
        self.style.configure("Header.TLabel",
            font=("Helvetica", 24, "bold"),
            padding=20,
            foreground="#2c3e50"
        )
        
        # Frame style
        self.style.configure("Card.TFrame",
            background="white",
            relief="flat"
        )
        
        # Button styles
        self.style.configure("Primary.TButton",
            padding=(20, 10),
            font=("Helvetica", 10, "bold")
        )
        
        self.style.configure("Tab.TNotebook",
            padding=10,
            tabposition="n"
        )
        
        # Entry style
        self.style.configure("Custom.TEntry",
            padding=10,
            fieldbackground="white"
        )

    def create_header(self):
        header = ttk.Label(
            self.main_container,
            text="Library Management System",
            style="Header.TLabel"
        )
        header.grid(row=0, column=0, pady=(0, 20), sticky="ew")

    def create_tabs(self):
        self.notebook = ttk.Notebook(self.main_container, style="Tab.TNotebook")
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Create tabs
        self.books_tab = self.create_books_tab()
        self.circulation_tab = self.create_circulation_tab()
        self.search_tab = self.create_search_tab()
        self.users_tab = self.create_users_tab()
        
        # Add tabs to notebook
        self.notebook.add(self.books_tab, text="Books Management")
        self.notebook.add(self.circulation_tab, text="Circulation")
        self.notebook.add(self.search_tab, text="Search")
        self.notebook.add(self.users_tab, text="User Records")

    def create_books_tab(self):
        tab = ttk.Frame(self.notebook, style="Card.TFrame", padding=20)
        
        # Add Book Form
        ttk.Label(tab, text="Add New Book", font=("Helvetica", 16, "bold")).grid(row=0, column=0, pady=(0, 20), sticky="w")
        
        fields = [("Book Title:", "book_title"), ("Author Name:", "book_author"), ("ISBN:", "book_isbn")]
        
        for i, (label, attr) in enumerate(fields):
            ttk.Label(tab, text=label).grid(row=i+1, column=0, pady=5, sticky="w")
            entry = ttk.Entry(tab, width=40, style="Custom.TEntry")
            entry.grid(row=i+1, column=1, pady=5, padx=10, sticky="ew")
            setattr(self, f"{attr}_entry", entry)
        
        ttk.Button(
            tab,
            text="Add Book",
            style="Primary.TButton",
            command=self.add_book
        ).grid(row=4, column=0, columnspan=2, pady=20)
        
        return tab

    def create_circulation_tab(self):
        tab = ttk.Frame(self.notebook, style="Card.TFrame", padding=20)
        
        # Borrow Section
        ttk.Label(tab, text="Borrow Book", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")
        
        ttk.Label(tab, text="User ID:").grid(row=1, column=0, pady=5, sticky="w")
        self.user_id_entry = ttk.Entry(tab, width=40, style="Custom.TEntry")
        self.user_id_entry.grid(row=1, column=1, pady=5, padx=10, sticky="ew")
        
        ttk.Label(tab, text="Book ISBN:").grid(row=2, column=0, pady=5, sticky="w")
        self.book_isbn_borrow_entry = ttk.Entry(tab, width=40, style="Custom.TEntry")
        self.book_isbn_borrow_entry.grid(row=2, column=1, pady=5, padx=10, sticky="ew")
        
        ttk.Button(
            tab,
            text="Borrow Book",
            style="Primary.TButton",
            command=self.borrow_book
        ).grid(row=3, column=0, columnspan=2, pady=20)
        
        # Return Section
        ttk.Label(tab, text="Return Book", font=("Helvetica", 16, "bold")).grid(row=4, column=0, columnspan=2, pady=(20, 20), sticky="w")
        
        ttk.Label(tab, text="Book ISBN:").grid(row=5, column=0, pady=5, sticky="w")
        self.book_isbn_return_entry = ttk.Entry(tab, width=40, style="Custom.TEntry")
        self.book_isbn_return_entry.grid(row=5, column=1, pady=5, padx=10, sticky="ew")
        
        ttk.Button(
            tab,
            text="Return Book",
            style="Primary.TButton",
            command=self.return_book
        ).grid(row=6, column=0, columnspan=2, pady=20)
        
        return tab

    def create_search_tab(self):
        tab = ttk.Frame(self.notebook, style="Card.TFrame", padding=20)
        
        ttk.Label(tab, text="Search Books", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")
        
        ttk.Label(tab, text="Search Term:").grid(row=1, column=0, pady=5, sticky="w")
        self.search_book_entry = ttk.Entry(tab, width=40, style="Custom.TEntry")
        self.search_book_entry.grid(row=1, column=1, pady=5, padx=10, sticky="ew")
        
        ttk.Button(
            tab,
            text="Search",
            style="Primary.TButton",
            command=self.search_book
        ).grid(row=2, column=0, columnspan=2, pady=20)
        
        # Add results treeview
        self.search_results = ttk.Treeview(tab, columns=("Title", "Author", "ISBN", "Status"), show="headings", height=10)
        self.search_results.grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")
        
        # Configure columns
        for col in ("Title", "Author", "ISBN", "Status"):
            self.search_results.heading(col, text=col)
            self.search_results.column(col, width=150)
        
        return tab

    def create_users_tab(self):
        tab = ttk.Frame(self.notebook, style="Card.TFrame", padding=20)
        
        ttk.Label(tab, text="User Records", font=("Helvetica", 16, "bold")).grid(row=0, column=0, pady=(0, 20), sticky="w")
        
        # Add user records treeview
        self.user_records = ttk.Treeview(tab, columns=("ID", "Name", "Books", "Status"), show="headings", height=15)
        self.user_records.grid(row=1, column=0, pady=10, sticky="nsew")
        
        # Configure columns
        for col in ("ID", "Name", "Books", "Status"):
            self.user_records.heading(col, text=col)
            self.user_records.column(col, width=150)
        
        ttk.Button(
            tab,
            text="Refresh Records",
            style="Primary.TButton",
            command=self.view_user_records
        ).grid(row=2, column=0, pady=20)
        
        return tab

    # Core functionality methods
    def add_book(self):
        title = self.book_title_entry.get()
        author = self.book_author_entry.get()
        isbn = self.book_isbn_entry.get()

        if title and author and isbn:
            book = {
                "isbn": isbn,
                "title": title,
                "author": author,
                "available": True,
                "due_date": None
            }
            self.books_collection.insert_one(book)
            messagebox.showinfo("Success", f"Book '{title}' added successfully.")
            
            # Clear the entries after successful addition
            self.book_title_entry.delete(0, tk.END)
            self.book_author_entry.delete(0, tk.END)
            self.book_isbn_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def borrow_book(self):
        user_id = self.user_id_entry.get()
        isbn = self.book_isbn_borrow_entry.get()

        if user_id and isbn:
            book = self.books_collection.find_one({"isbn": isbn})

            if book and book["available"]:
                user = self.users_collection.find_one({"user_id": user_id})

                if not user:
                    self.users_collection.insert_one({"user_id": user_id, "name": user_id})

                due_date = datetime.now() + timedelta(days=7)
                self.books_collection.update_one({"isbn": isbn}, {"$set": {"available": False, "due_date": due_date}})
                self.borrowed_books_collection.insert_one({"user_id": user_id, "isbn": isbn})
                messagebox.showinfo("Success", "Book borrowed successfully.")
                
                # Clear the entries after successful borrowing
                self.user_id_entry.delete(0, tk.END)
                self.book_isbn_borrow_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Book not available or not found.")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def return_book(self):
        isbn = self.book_isbn_return_entry.get()

        if isbn:
            book = self.books_collection.find_one({"isbn": isbn})

            if book:
                self.borrowed_books_collection.delete_one({"isbn": isbn})
                self.books_collection.update_one({"isbn": isbn}, {"$set": {"available": True, "due_date": None}})
                messagebox.showinfo("Success", "Book returned successfully.")
                
                # Clear the entry after successful return
                self.book_isbn_return_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Book not found.")
        else:
            messagebox.showerror("Error", "Please enter a book ISBN.")

    def search_book(self):
        search_term = self.search_book_entry.get().lower()
        
        # Clear existing items in treeview
        for item in self.search_results.get_children():
            self.search_results.delete(item)
            
        if search_term:
            books = self.books_collection.find({
                "$or": [
                    {"title": {"$regex": search_term, "$options": "i"}},
                    {"author": {"$regex": search_term, "$options": "i"}},
                    {"isbn": {"$regex": search_term, "$options": "i"}}
                ]
            })
            
            for book in books:
                status = "Available" if book["available"] else "Borrowed"
                self.search_results.insert("", "end", values=(
                    book["title"],
                    book["author"],
                    book["isbn"],
                    status
                ))
        else:
            messagebox.showwarning("Warning", "Please enter a search term.")

    def view_user_records(self):
        # Clear existing items in treeview
        for item in self.user_records.get_children():
            self.user_records.delete(item)
            
        users = self.users_collection.find()
        
        for user in users:
            user_id = user["user_id"]
            name = user["name"]
            borrowed_books = list(self.borrowed_books_collection.find({"user_id": user_id}))
            
            books_info = []
            status = "Active" if borrowed_books else "No books borrowed"
            
            for record in borrowed_books:
                book = self.books_collection.find_one({"isbn": record["isbn"]})
                if book:
                    books_info.append(book["title"])
            
            self.user_records.insert("", "end", values=(
                user_id,
                name,
                ", ".join(books_info) if books_info else "None",
                status
            ))
#main 
if _name_ == "_main_":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()
