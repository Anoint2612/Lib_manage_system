import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
from pymongo import MongoClient

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1024x768")
        self.root.configure(bg="#ffffff")

        # MongoDB setup remains the same
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["library_db"]
        self.books_collection = self.db["books"]
        self.users_collection = self.db["users"]
        self.borrowed_books_collection = self.db["borrowed_books"]
        
        # Configure modern styles
        self.setup_styles()
        
        # Create main container with padding
        self.main_container = ttk.Frame(self.root, padding="30")
        self.main_container.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights for responsiveness
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Create header and tabs
        self.create_header()
        self.create_tabs()

    def setup_styles(self):
        self.style = ttk.Style()
        
        # Modern color palette
        self.colors = {
            'primary': '#2563eb',      # Blue
            'secondary': '#64748b',    # Slate
            'success': '#22c55e',      # Green
            'background': '#ffffff',   # White
            'surface': '#f8fafc',      # Light gray
            'text': '#1e293b',         # Dark slate
            'border': '#e2e8f0'        # Light border
        }
        
        # Configure general style
        self.style.configure(".",
            background=self.colors['background'],
            foreground=self.colors['text'],
            font=("Inter", 10)
        )
        
        # Modern header style
        self.style.configure("Header.TLabel",
            font=("Inter", 28, "bold"),
            padding=20,
            foreground=self.colors['primary']
        )
        
        # Card style frame
        self.style.configure("Card.TFrame",
            background=self.colors['surface'],
            relief="flat",
            borderwidth=1
        )
        
        # Modern button style
        self.style.configure("Primary.TButton",
            padding=(20, 12),
            font=("Inter", 10, "bold"),
            background=self.colors['primary'],
            foreground="white"
        )
        
        # Modern entry style
        self.style.configure("Custom.TEntry",
            padding=12,
            fieldbackground=self.colors['background'],
            borderwidth=1,
            relief="solid"
        )
        
        # Notebook (tabs) style
        self.style.configure("Custom.TNotebook",
            background=self.colors['background'],
            padding=10,
            tabmargins=[2, 5, 2, 0]
        )
        
        self.style.configure("Custom.TNotebook.Tab",
            padding=[15, 8],
            font=("Inter", 10),
            background=self.colors['surface'],
            foreground=self.colors['text']
        )
        
        # Treeview style
        self.style.configure("Treeview",
            background=self.colors['background'],
            fieldbackground=self.colors['background'],
            font=("Inter", 10),
            rowheight=40
        )
        
        self.style.configure("Treeview.Heading",
            font=("Inter", 10, "bold"),
            background=self.colors['surface'],
            padding=10
        )

    def create_header(self):
        header = ttk.Label(
            self.main_container,
            text="Library Management System",
            style="Header.TLabel"
        )
        header.grid(row=0, column=0, pady=(0, 20), sticky="ew")

    def create_tabs(self):
        self.notebook = ttk.Notebook(self.main_container, style="Custom.TNotebook")
        self.notebook.grid(row=1, column=0, sticky="nsew")
        
        # Create and add tabs
        self.books_tab = self.create_books_tab()
        self.circulation_tab = self.create_circulation_tab()
        self.search_tab = self.create_search_tab()
        self.users_tab = self.create_users_tab()
        
        self.notebook.add(self.books_tab, text="📚 Books")
        self.notebook.add(self.circulation_tab, text="🔄 Circulation")
        self.notebook.add(self.search_tab, text="🔍 Search")
        self.notebook.add(self.users_tab, text="👥 Users")

    def create_books_tab(self):
        tab = ttk.Frame(self.notebook, style="Card.TFrame", padding=30)
        tab.grid_columnconfigure(1, weight=1)
        
        # Section title with icon
        title_frame = ttk.Frame(tab)
        title_frame.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 30))
        
        ttk.Label(
            title_frame,
            text="Add New Book",
            font=("Inter", 18, "bold"),
            foreground=self.colors['primary']
        ).grid(row=0, column=0, sticky="w")
        
        # Form fields
        fields = [
            ("📖 Book Title:", "book_title"),
            ("✍ Author Name:", "book_author"),
            ("🏷 ISBN:", "book_isbn")
        ]
        
        for i, (label, attr) in enumerate(fields):
            ttk.Label(
                tab,
                text=label,
                font=("Inter", 10)
            ).grid(row=i+1, column=0, pady=12, padx=(0, 15), sticky="w")
            
            entry = ttk.Entry(
                tab,
                width=40,
                style="Custom.TEntry"
            )
            entry.grid(row=i+1, column=1, pady=12, sticky="ew")
            setattr(self, f"{attr}_entry", entry)
        
        # Add book button
        button_frame = ttk.Frame(tab)
        button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=30)
        
        ttk.Button(
            button_frame,
            text="Add Book",
            style="Primary.TButton",
            command=self.add_book
        ).grid(row=0, column=0)
        
        return tab

    def create_circulation_tab(self):
        tab = ttk.Frame(self.notebook, style="Card.TFrame", padding=30)
        tab.grid_columnconfigure(1, weight=1)
        
        # Borrow Section
        ttk.Label(
            tab,
            text="Borrow Book",
            font=("Inter", 18, "bold"),
            foreground=self.colors['primary']
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 30))
        
        # Borrow form fields
        ttk.Label(tab, text="👤 User ID:").grid(row=1, column=0, pady=12, padx=(0, 15), sticky="w")
        self.user_id_entry = ttk.Entry(tab, width=40, style="Custom.TEntry")
        self.user_id_entry.grid(row=1, column=1, pady=12, sticky="ew")
        
        ttk.Label(tab, text="📚 Book ISBN:").grid(row=2, column=0, pady=12, padx=(0, 15), sticky="w")
        self.book_isbn_borrow_entry = ttk.Entry(tab, width=40, style="Custom.TEntry")
        self.book_isbn_borrow_entry.grid(row=2, column=1, pady=12, sticky="ew")
        
        ttk.Button(
            tab,
            text="Borrow Book",
            style="Primary.TButton",
            command=self.borrow_book
        ).grid(row=3, column=0, columnspan=2, pady=30)
        
        # Return Section
        ttk.Label(
            tab,
            text="Return Book",
            font=("Inter", 18, "bold"),
            foreground=self.colors['primary']
        ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(30, 30))
        
        ttk.Label(tab, text="📚 Book ISBN:").grid(row=5, column=0, pady=12, padx=(0, 15), sticky="w")
        self.book_isbn_return_entry = ttk.Entry(tab, width=40, style="Custom.TEntry")
        self.book_isbn_return_entry.grid(row=5, column=1, pady=12, sticky="ew")
        
        ttk.Button(
            tab,
            text="Return Book",
            style="Primary.TButton",
            command=self.return_book
        ).grid(row=6, column=0, columnspan=2, pady=30)
        
        return tab

    def create_search_tab(self):
        tab = ttk.Frame(self.notebook, style="Card.TFrame", padding=30)
        tab.grid_columnconfigure(1, weight=1)
        
        # Search section title
        ttk.Label(
            tab,
            text="Search Books",
            font=("Inter", 18, "bold"),
            foreground=self.colors['primary']
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 30))
        
        # Search field
        ttk.Label(tab, text="🔍 Search:").grid(row=1, column=0, pady=12, padx=(0, 15), sticky="w")
        self.search_book_entry = ttk.Entry(tab, width=40, style="Custom.TEntry")
        self.search_book_entry.grid(row=1, column=1, pady=12, sticky="ew")
        
        # Search button
        ttk.Button(
            tab,
            text="Search",
            style="Primary.TButton",
            command=self.search_book
        ).grid(row=2, column=0, columnspan=2, pady=30)
        
        # Results table
        self.search_results = ttk.Treeview(
            tab,
            columns=("Title", "Author", "ISBN", "Status"),
            show="headings",
            height=10,
            style="Treeview"
        )
        self.search_results.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=10)
        
        # Configure columns with modern styling
        for col in ("Title", "Author", "ISBN", "Status"):
            self.search_results.heading(col, text=col)
            self.search_results.column(col, width=150, anchor="center")
        
        return tab

    def create_users_tab(self):
        tab = ttk.Frame(self.notebook, style="Card.TFrame", padding=20)
        
        # Configure grid weights for the tab
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)  # Make the treeview expandable
        
        ttk.Label(tab, text="User Records", font=("Helvetica", 16, "bold")).grid(
            row=0, column=0, pady=(0, 20), sticky="w"
        )
        
        # Add user records treeview
        self.user_records = ttk.Treeview(
            tab, 
            columns=("ID", "Name", "Books", "Status"), 
            show="headings", 
            height=10
        )
        self.user_records.grid(row=1, column=0, sticky="nsew", padx=5)
        
        # Configure columns
        for col in ("ID", "Name", "Books", "Status"):
            self.user_records.heading(col, text=col)
            self.user_records.column(col, width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=self.user_records.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.user_records.configure(yscrollcommand=scrollbar.set)
        
        # Refresh button - ensure it's visible at the bottom
        refresh_button = ttk.Button(
            tab,
            text="Refresh Records",
            style="Primary.TButton",
            command=self.view_user_records
        )
        refresh_button.grid(row=2, column=0, pady=20, padx=5, sticky="ew")
        
        return tab

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
# Allows a user to borrow a book by marking it as unavailable in the database and creating a borrowing record.

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
# Allows a user to return a borrowed book by marking it as available in the database and removing the borrowing record.

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
# Searches for books in the library database based on a search term and displays the results in a table.

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
# Displays all registered users along with their borrowed book details in the User Records tab.

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
# Entry point: Creates the main application window and starts the Tkinter event loop.

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()
