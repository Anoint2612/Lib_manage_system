# Library Management System

A comprehensive library management system written in Python, designed to streamline the management of books, users, and their borrowing activities. The system leverages JSON files to store data for books and users, ensuring simplicity and ease of data access.

---

## Features

### Book Management
- **Add New Books**: Seamlessly add new books to the library’s collection.
- **Remove Books**: Easily remove books no longer available or relevant.
- **Update Book Details**: Modify book details such as quantity, title, or author.
- **Search Books**: Locate books quickly by title, author, or ISBN.

### User Management
- **Register New Users**: Facilitate easy user registration to maintain user records.
- **Borrow Books**: Allow users to borrow books from the library’s collection.
- **Return Books**: Track and manage the return of borrowed books.
- **List Borrowed Books**: View a detailed list of books borrowed by each user.

### Overdue Notifications
- **Track Overdue Books**: Monitor borrowed books and identify overdue returns.
- **Notify Users**: Alert users with notifications about overdue books, ensuring timely returns.

---

## File Structure

### Example: `books.json`
```json
[
  {
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": "9780743273565",
    "quantity": 5
  }
]

