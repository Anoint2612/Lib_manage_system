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
