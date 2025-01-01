# Library Management System

A simple library management system written in Python, designed to manage books, users, and their borrowing activities. It includes functionalities to add, remove, and search for books, as well as manage user registrations, borrowing, and returning of books. The system stores data in JSON files for books and users.

## Features

- **Book Management**:
  - Add new books to the library.
  - Remove books from the library.
  - Update book details (e.g., quantity, title, author).
  - Search books by title, author, or ISBN.

- **User Management**:
  - Register new users.
  - Borrow books from the library.
  - Return borrowed books.
  - List borrowed books for each user.

- **Overdue Notifications**:
  - Track overdue books and notify users if they have overdue books.

## File Structure

- `books.json` - Stores book data (title, author, ISBN, quantity).
- `users.json` - Stores user data (user ID, name, borrowed books).

### Example of `books.json`:
```json
[
  {
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": "9780743273565",
    "quantity": 5
  },
  {
    "title": "1984",
    "author": "George Orwell",
    "isbn": "9780451524935",
    "quantity": 3
  }
]
## Example of `users.json`:
```json
[
  {
    "user_id": 1,
    "name": "John Doe"
  },
  {
    "user_id": 2,
    "name": "Jane Smith"
  }
]

## Classes

### 1. `Book`
This class represents a book in the library. It stores details such as the title, author, ISBN, and quantity. It has methods for:
- Converting the book object to a dictionary for JSON serialization.
- Returning a string representation of the book.

### 2. `User`
This class represents a user of the library. It stores details such as user ID, name, and borrowed books. It has methods for:
- Borrowing books with due dates.
- Returning borrowed books.
- Listing borrowed books.

### 3. `Library`
This class manages the collection of books and users. It supports functionalities like:
- Adding, removing, and updating books.
- Registering users.
- Borrowing and returning books.
- Checking for overdue books and sending notifications.

---

## Usage

To use the Library Management System, you can run the Python script `library_management_system.py`. Here's an example of how the system works.

### Example Usage

```python
from datetime import datetime
import json

# Initialize Library
library = Library()

# Add some books
library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", 5)
library.add_book("1984", "George Orwell", "9780451524935", 3)
library.add_book("To Kill a Mockingbird", "Harper Lee", "9780061120084", 2)

# Register users
library.register_user(1, "John Doe")
library.register_user(2, "Jane Smith")

# Borrow books
library.borrow_book(1, "9780743273565")  # John borrows The Great Gatsby
library.borrow_book(2, "9780451524935")  # Jane borrows 1984

# List borrowed books for a user
library.users[1].list_borrowed_books()

# Return a borrowed book
library.return_book(1, "9780743273565")  # John returns The Great Gatsby

# Check for overdue books
library.notify_overdue()

# Search for books by title
search_results = library.search_books(title="1984")
for book in search_results:
    print(book)

# Remove a book from the library
library.remove_book("9780061120084")  # Remove "To Kill a Mockingbird"

# Update book details
library.update_book("9780451524935", quantity=5)