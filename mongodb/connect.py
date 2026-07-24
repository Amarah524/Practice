from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["LibraryDB"]
books = db["Books"]
def add_book():
    print("\n==== Add Book ====")
    title = input("Enter title: ")
    author = input("Enter author: ")
    price = int(input("Enter price: "))
    available = input("Is the book available? (yes/no): ").lower()
    if available == "yes":
        available = True
    else:
        available = False

    book = {
        "title": title,
        "author": author,
        "price": price,
        "available": available
    }

    result = books.insert_one(book)
    print("Book added successfully!")
    print("Inserted ID:", result.inserted_id)

def view_books():
    print("\n==== All Books ====")
    if books.count_documents({}) == 0:
        print("No books found")
        return
    for book in books.find():
        print("Title:", book["title"])
        print("Author:", book["author"])
        print("Price:", book["price"])
        print("Available:", book["available"])

def search_book():

    print("\n===== Search Book =====")

    title = input("Enter Book Title: ")

    book = books.find_one({"title": title})

    if book:

        print("\nBook Found")
        print("---------------------------")
        print("Title:", book["title"])
        print("Author:", book["author"])
        print("Price:", book["price"])
        print("Available:", book["available"])
        print("---------------------------")

    else:

        print("Book Not Found.")



def update_book():

    print("\n===== Update Book =====")

    title = input("Enter Book Title: ")

    new_price = int(input("Enter New Price: "))

    result = books.update_one(
        {"title": title},
        {"$set": {"price": new_price}}
    )

    if result.modified_count > 0:

        print("Book Updated Successfully!")

    else:

        print("Book Not Found.")


def delete_book():

    print("\n===== Delete Book =====")

    title = input("Enter Book Title: ")

    result = books.delete_one(
        {"title": title}
    )

    if result.deleted_count > 0:

        print("Book Deleted Successfully!")

    else:

        print("Book Not Found.")

def count_books():

    total = books.count_documents({})

    print("\nTotal Books:", total)

while True:

    print("\n===== Library Management System =====")
    print("1. Add Book")
    print("2. View All Books")
    print("3. Search Book")
    print("4. Update Book Price")
    print("5. Delete Book")
    print("6. Count Books")
    print("7. Exit")

    choice = input("\nEnter Your Choice: ")

    if choice == "1":

        add_book()

    elif choice == "2":

        view_books()

    elif choice == "3":

        search_book()

    elif choice == "4":

        update_book()

    elif choice == "5":

        delete_book()

    elif choice == "6":

        count_books()

    elif choice == "7":

        print("\nThank You!")
        print("Program Closed Successfully.")
        break

    else:

        print("\nInvalid Choice. Please Try Again.")