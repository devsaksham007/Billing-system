import math
import random
from datetime import datetime, timedelta


class LibraryError(Exception):
    """Base exception for library operations."""


class BookNotFoundError(LibraryError):
    pass


class BookUnavailableError(LibraryError):
    pass


class MemberNotFoundError(LibraryError):
    pass


class Book:
    def __init__(self, title, author, isbn):
        if not title.strip() or not author.strip() or not isbn.strip():
            raise ValueError("Title, author, and ISBN are required")

        self.title = title.strip()
        self.author = author.strip()
        self.isbn = isbn.strip()
        self.is_issued = False

    def display_details(self):
        status = "Issued" if self.is_issued else "Available"
        return f"{self.title} by {self.author} | ISBN: {self.isbn} | {status}"


class EBook(Book):
    def __init__(self, title, author, isbn, file_size_mb):
        super().__init__(title, author, isbn)
        if file_size_mb <= 0:
            raise ValueError("File size must be positive")
        self.file_size_mb = float(file_size_mb)

    def display_details(self):
        return f"{super().display_details()} | Digital: {self.file_size_mb:.1f} MB"


class LibraryMember:
    def __init__(self, name, member_id=None):
        if not name.strip():
            raise ValueError("Member name is required")

        self.name = name.strip()
        self.member_id = member_id or f"M-{random.randint(1000, 9999)}"
        self.borrowed_books = {}

    def borrowed_count(self):
        return len(self.borrowed_books)


class Library:
    LOAN_DAYS = 14

    def __init__(self, name):
        self.name = name
        self.books = {}
        self.members = {}

    def add_book(self, book):
        if book.isbn in self.books:
            raise LibraryError(f"A book with ISBN {book.isbn} already exists")
        self.books[book.isbn] = book

    def remove_book(self, isbn):
        book = self._get_book(isbn)
        if book.is_issued:
            raise BookUnavailableError("Issued books cannot be removed")
        del self.books[isbn]

    def register_member(self, member):
        if member.member_id in self.members:
            raise LibraryError(f"Member ID {member.member_id} already exists")
        self.members[member.member_id] = member

    def issue_book(self, isbn, member_id):
        book = self._get_book(isbn)
        member = self._get_member(member_id)
        if book.is_issued:
            raise BookUnavailableError(f"'{book.title}' is already issued")

        book.is_issued = True
        due_date = datetime.now() + timedelta(days=self.LOAN_DAYS)
        member.borrowed_books[isbn] = due_date
        return due_date

    def return_book(self, isbn, member_id):
        book = self._get_book(isbn)
        member = self._get_member(member_id)
        if isbn not in member.borrowed_books:
            raise LibraryError("This member did not borrow that book")

        due_date = member.borrowed_books.pop(isbn)
        book.is_issued = False
        overdue_days = max(0, (datetime.now() - due_date).days)
        late_fee = math.ceil(overdue_days * 0.50)
        return late_fee

    def list_books(self):
        return [book.display_details() for book in self.books.values()]

    def _get_book(self, isbn):
        if isbn not in self.books:
            raise BookNotFoundError(f"No book found with ISBN {isbn}")
        return self.books[isbn]

    def _get_member(self, member_id):
        if member_id not in self.members:
            raise MemberNotFoundError(f"No member found with ID {member_id}")
        return self.members[member_id]


def demo():
    library = Library("Central Library")
    library.add_book(Book("The Hobbit", "J.R.R. Tolkien", "978-0261102217"))
    library.add_book(EBook("Clean Code", "Robert C. Martin", "978-0132350884", 5.8))

    member = LibraryMember("Alex", "M-1001")
    library.register_member(member)

    due_date = library.issue_book("978-0261102217", member.member_id)
    print(f"Issued to {member.name}; due on {due_date:%Y-%m-%d}")
    print("Books:")
    for book_details in library.list_books():
        print(f"- {book_details}")

    try:
        library.issue_book("978-0261102217", member.member_id)
    except LibraryError as error:
        print(f"Handled error: {error}")

    late_fee = library.return_book("978-0261102217", member.member_id)
    print(f"Returned successfully; late fee: ${late_fee:.2f}")


if __name__ == "__main__":
    demo()