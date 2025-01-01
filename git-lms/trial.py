import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime, timedelta
from pymongo import MongoClient

# Class to represent a Book
class Book:
    def __init__(self, title, author, isbn, available=True):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = available
        self.due_date = None

# Class to represent a User
class User:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

# Main Library Management System Class with the GUI
class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("600x600")  # Adjusted size for more space

        # Connect to MongoDB
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["library_db"]
        self.books_collection = self.db["books"]
        self.users_collection = self.db["users"]
        self.borrowed_books_collection = self.db["borrowed_books"]
        self.initialize_database()

        # Apply modern ttk styles
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat", background="#4CAF50", foreground="white", font=("Helvetica", 10))
        self.style.configure("TLabel", font=("Helvetica", 12), padding=6)

        # Create the GUI elements
        self.create_widgets()

    def initialize_database(self):
        # MongoDB automatically handles collections and indexes, so no need for schema creation.
        pass

    def create_widgets(self):
        # Create frames for organization
        self.frame1 = ttk.LabelFrame(self.root, text="Add Book", padding=(20, 10))
        self.frame1.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        self.frame2 = ttk.LabelFrame(self.root, text="Borrow Book", padding=(20, 10))
        self.frame2.grid(row=1, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        self.frame3 = ttk.LabelFrame(self.root, text="Return Book", padding=(20, 10))
        self.frame3.grid(row=2, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        self.frame4 = ttk.LabelFrame(self.root, text="Search Book", padding=(20, 10))
        self.frame4.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        self.frame5 = ttk.LabelFrame(self.root, text="Manage User Records", padding=(20, 10))
        self.frame5.grid(row=4, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        # Add Book Section
        ttk.Label(self.frame1, text="Book Title:").grid(row=0, column=0, sticky="w")
        self.book_title_entry = ttk.Entry(self.frame1, width=30)
        self.book_title_entry.grid(row=0, column=1, padx=10)

        ttk.Label(self.frame1, text="Author Name:").grid(row=1, column=0, sticky="w")
        self.book_author_entry = ttk.Entry(self.frame1, width=30)
        self.book_author_entry.grid(row=1, column=1, padx=10)

        ttk.Label(self.frame1, text="ISBN:").grid(row=2, column=0, sticky="w")
        self.book_isbn_entry = ttk.Entry(self.frame1, width=30)
        self.book_isbn_entry.grid(row=2, column=1, padx=10)

        self.add_book_button = ttk.Button(self.frame1, text="Add Book", command=self.add_book)
        self.add_book_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Borrow Book Section
        ttk.Label(self.frame2, text="User ID:").grid(row=0, column=0, sticky="w")
        self.user_id_entry = ttk.Entry(self.frame2, width=30)
        self.user_id_entry.grid(row=0, column=1, padx=10)

        ttk.Label(self.frame2, text="Book ISBN:").grid(row=1, column=0, sticky="w")
        self.book_isbn_borrow_entry = ttk.Entry(self.frame2, width=30)
        self.book_isbn_borrow_entry.grid(row=1, column=1, padx=10)

        self.borrow_book_button = ttk.Button(self.frame2, text="Borrow Book", command=self.borrow_book)
        self.borrow_book_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Return Book Section
        ttk.Label(self.frame3, text="Book ISBN:").grid(row=0, column=0, sticky="w")
        self.book_isbn_return_entry = ttk.Entry(self.frame3, width=30)
        self.book_isbn_return_entry.grid(row=0, column=1, padx=10)

        self.return_book_button = ttk.Button(self.frame3, text="Return Book", command=self.return_book)
        self.return_book_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Search Book Section
        ttk.Label(self.frame4, text="Search Term:").grid(row=0, column=0, sticky="w")
        self.search_book_entry = ttk.Entry(self.frame4, width=30)
        self.search_book_entry.grid(row=0, column=1, padx=10)

        self.search_book_button = ttk.Button(self.frame4, text="Search Book", command=self.search_book)
        self.search_book_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Manage User Records Section
        self.view_user_button = ttk.Button(self.frame5, text="View User Records", command=self.view_user_records)
        self.view_user_button.grid(row=0, column=0, columnspan=2, pady=10)

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
            else:
                messagebox.showerror("Error", "Book not found.")
        else:
            messagebox.showerror("Error", "Please enter a book ISBN.")

    def search_book(self):
        search_term = self.search_book_entry.get().lower()
        books = self.books_collection.find({
            "$or": [
                {"title": {"$regex": search_term, "$options": "i"}},
                {"author": {"$regex": search_term, "$options": "i"}}
            ]
        })
        
        # Convert cursor to a list to count the number of books
        book_list = list(books)
        
        if len(book_list) > 0:  # Check the length of the list
            result_text = "\n".join([f"{book['title']} by {book['author']} (ISBN: {book['isbn']})" for book in book_list])
            messagebox.showinfo("Search Results", result_text)
        else:
            messagebox.showinfo("Search Results", "No books found.")


    def view_user_records(self):
        users = self.users_collection.find()
        records = []

        for user in users:
            user_id = user["user_id"]
            name = user["name"]
            borrowed_books = self.borrowed_books_collection.find({"user_id": user_id})

            borrowed_info = ""
            overdue_info = ""
            for record in borrowed_books:
                book = self.books_collection.find_one({"isbn": record["isbn"]})
                if book:
                    due_date = book.get("due_date")
                    if due_date and due_date < datetime.now():
                        overdue_info += f"{book['title']} (Overdue: {due_date})\n"
                    borrowed_info += f"{book['title']} (Due: {due_date})\n"

            record = f"User ID: {user_id}\nName: {name}\nBorrowed Books:\n{borrowed_info}\nOverdue Books:\n{overdue_info}\n"
            records.append(record)

        messagebox.showinfo("User Records", "\n\n".join(records))

# Main code to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()
