import mysql.connector
from datetime import date, timedelta

sql_connector = mysql.connector.connect(
    host="localhost", user="root", passwd="admin", database="mysql"
)
sql_cursor = sql_connector.cursor()
while True:
    id = str(input("Enter your Username: "))
    pwd = str(input("Enter your Password: "))
    if id == "admin" and pwd == "admin":
        try:
            sql_cursor.execute("CREATE DATABASE Library")
            sql_cursor.execute("USE Library")
            sql_cursor.execute(
                "CREATE TABLE Lended (Book_ID INT, "
                "Account_ID INT, Date_Borrowed CHAR(10), Date_Return CHAR(10))"
            )
            sql_cursor.execute(
                "CREATE TABLE Accounts (Account_ID INT, Account_Name CHAR(20), Phone BIGINT)"
            )
            sql_cursor.execute(
                "CREATE TABLE Catalog (Book_ID INT, Book_Name CHAR(50), Author_Name CHAR(20), Qty INT)"
            )
            sql = "INSERT INTO Accounts VALUES (%s,%s,%s)"
            val = [
                (100, "Ritu Bari", 8798282309),
                (101, "Vishakha Chauhan", 8964382373),
                (102, "Shivansh Goel", 9872546824),
                (103, "Mayank Chaurasia", 9628423512),
                (104, "Kanishka Jain", 9234548994),
            ]
            sql_cursor.executemany(sql, val)
            sql_connector.commit()
            sql2 = "INSERT INTO Catalog VALUES (%s,%s,%s,%s)"
            val2 = [
                (5000, "To Kill a Mockingbird", "Harper Lee", 3),
                (5001, "1984", "George Orwell", 8),
                (5002, "Harry Potter and the Philosopher’s Stone", "J.K. Rowling", 1),
                (5003, "The Lord of the Rings", "J.R.R. Tolkien", 3),
                (5004, "The Great Gatsby", "F. Scott Fitzgerald", 6),
            ]
            sql_cursor.executemany(sql2, val2)
            sql_connector.commit()
        except:
            pass
        finally:
            sql_cursor.execute("USE Library")
        while True:
            print("")
            print("Choose an Option")
            print("1. Lend a Book")
            print("2. Create New Borrower Account")
            print("3. Add a New Book to the Catalog")
            print("4. Delete a Book from the Catalog")
            menu1 = int(input(">> "))
            print("")
            if menu1 == 1:
                print("Lend a Book".center(130))
                print("")
                menu5 = input("Enter Book ID: ")
                menu6 = input("Enter Account ID: ")
                menu7 = int(input("Enter No. of Days Book is borrowed for: "))
                today = date.today()
                date = today.strftime("%d/%m/%Y")
                due = today + timedelta(menu7)
                duef = due.strftime("%d/%m/%Y")
                sql3 = "INSERT INTO Lended VALUES (%s,%s,%s,%s)"
                val3 = [(menu5, menu6, date, duef)]
                sql_cursor.executemany(sql3, val3)
                sql_connector.commit()
                sql_cursor.execute(
                    "UPDATE Catalog SET Qty=Qty-1 where Book_ID=" + menu5
                )
                sql_connector.commit()
                print("")
                print("Book Issued".center(130))
            elif menu1 == 2:
                print("Create New Borrower Account".center(130))
                print("")
                name = str(input("Name of Account Holder: "))
                phone = int(input("Phone Number: "))
                while True:
                    confirm = str(input("Do want to proceed (Y/N): "))
                    if confirm.lower() == "y":
                        aid_f = open(r"D:\Library\Account_ID.log", "r")
                        aid_l = aid_f.readlines()
                        aid = int(aid_l[0])
                        aid_f.close()
                        aid += 1
                        aid_f = open(r"D:\Library\Account_ID.log", "w")
                        aid_f.write(str(aid))
                        aid_f.close()
                        sql = "INSERT INTO Accounts VALUES (%s,%s,%s)"
                        val = [(aid, name, phone)]
                        sql_cursor.executemany(sql, val)
                        sql_connector.commit()

                        print(
                            (
                                "New ID has been created with User ID: " + str(aid)
                            ).center(130)
                        )
                        print("")
                        break
                    elif confirm.lower() == "n":
                        print("Request Canceled".center(130))
                        break
                    else:
                        print("Invalid Input".center(130))
                    print("")
            elif menu1 == 3:
                print("Add a New Book to the Catalog".center(130))
                print("")
                name = str(input("Name of the Book: "))
                aname = str(input("Author Name: "))
                qty = int(input("Quantity: "))
                while True:
                    confirm = str(input("Do want to proceed (Y/N): "))
                    if confirm.lower() == "y":
                        bid_f = open(r"D:\Library\Book_ID.log", "r")
                        bid_l = bid_f.readlines()
                        bid = int(bid_l[0])
                        bid_f.close()
                        bid += 1
                        bid_f = open(r"D:\Library\Book_ID.log", "w")
                        bid_f.write(str(bid))
                        bid_f.close()
                        sql = "INSERT INTO Catalog VALUES (%s,%s,%s,%s)"
                        val = [(bid, name, aname, qty)]
                        sql_cursor.executemany(sql, val)
                        sql_connector.commit()

                        print(
                            (
                                "New Book has been added to the Catalog with Book ID: "
                                + str(bid)
                            ).center(130)
                        )
                        print("")
                        break
                    elif confirm.lower() == "n":
                        print("Request Canceled".center(130))
                        break
                    else:
                        print("Invalid Input".center(130))
                    print("")
            elif menu1 == 4:
                print("Delete a Book from the Catalog".center(130))
                print("")
                print("How do you want to Search for the Book to be Deleted?")
                print("1. Book ID")
                print("2. Book Name")
                print("3. Author Name")
                menu_2 = int(input(">> "))
                if menu_2 == 1:
                    while True:
                        menu3 = int(input("Book ID: "))
                        try:
                            sql_cursor.execute(
                                "SELECT * FROM Catalog WHERE Book_ID=" + str(menu3)
                            )
                            record = sql_cursor.fetchall()
                            print(
                                "Do you wan to Delete", record[0][1], "by", record[0][2]
                            )
                            confirm = str(input("Do want to proceed (Y/N): "))
                            if confirm.lower() == "y":
                                while True:
                                    menu4 = int(input("Quantity to be Deleted: "))
                                    if menu4 <= record[0][3]:
                                        sql_cursor.execute(
                                            "UPDATE Catalog SET Qty="
                                            + str(record[0][3] - menu4)
                                            + " WHERE Book_ID="
                                            + str(menu3)
                                        )
                                        sql_connector.commit()
                                        print("Catalog Updated".center(130))
                                        break
                                    else:
                                        print(
                                            "Only",
                                            record[0][3],
                                            "Books are available".center(130),
                                        )
                                break
                            elif confirm.lower() == "n":
                                print("Request Canceled".center(130))
                                break
                            else:
                                print("Invalid Input".center(130))
                            print("")
                        except:
                            print("Book Doesn't Exists".center(130))
                elif menu_2 == 2:
                    while True:
                        menu3 = str(input("Book Name: "))
                        try:
                            sql_cursor.execute(
                                "SELECT * FROM Catalog WHERE Book_Name like '%"
                                + menu3
                                + "%'"
                            )
                            record = sql_cursor.fetchall()
                            print(
                                "Do you want to Delete",
                                record[0][1],
                                "by",
                                record[0][2],
                            )
                            confirm = str(input("Do want to proceed (Y/N): "))
                            if confirm.lower() == "y":
                                while True:
                                    menu4 = int(input("Quantity to be Deleted: "))
                                    if menu4 <= record[0][3]:
                                        sql_cursor.execute(
                                            "UPDATE Catalog SET Qty="
                                            + str(record[0][3] - menu4)
                                            + " WHERE Book_Name LIKE '%"
                                            + str(menu3)
                                            + "%'"
                                        )
                                        sql_connector.commit()
                                        print("Catalog Updated".center(130))
                                        break
                                    else:
                                        print(
                                            (
                                                "Only "
                                                + str(record[0][3])
                                                + " Books are available"
                                            ).center(130)
                                        )
                                break
                            elif confirm.lower() == "n":
                                print("Request Canceled".center(130))
                                break
                            else:
                                print("Invalid Input".center(130))
                            print("")
                        except:
                            print("Book Doesn't Exists".center(130))
                elif menu_2 == 3:
                    while True:
                        menu3 = str(input("Author Name: "))
                        try:
                            sql_cursor.execute(
                                "SELECT * FROM Catalog WHERE Author_Name LIKE '%"
                                + str(menu3)
                                + "%'"
                            )
                            record = sql_cursor.fetchall()
                            print(
                                "Do you want to Delete",
                                record[0][1],
                                "by",
                                record[0][2],
                            )
                            confirm = str(input("Do want to proceed (Y/N): "))
                            if confirm.lower() == "y":
                                while True:
                                    menu4 = int(input("Quantity to be Deleted: "))
                                    if menu4 <= record[0][3]:
                                        sql_cursor.execute(
                                            "UPDATE Catalog SET Qty="
                                            + str(record[0][3] - menu4)
                                            + " WHERE Author_Name like '%"
                                            + str(menu3)
                                            + "%'"
                                        )
                                        sql_connector.commit()
                                        print("Catalog Updated".center(130))
                                        break
                                    else:
                                        print(
                                            (
                                                "Only "
                                                + str(record[0][3])
                                                + " Books are available"
                                            ).center(130)
                                        )
                                break
                            elif confirm.lower() == "n":
                                print("Request Canceled".center(130))
                                break
                            else:
                                print("Invalid Input".center(130))
                            print("")
                        except:
                            print("Book Doesn't Exists".center(130))
            else:
                print("Invalid Input".center(130))
                print("")
        break
    elif id.lower() == "admin":
        print("")
        print("Wrong Password".center(130))
    else:
        print("")
        print("Wrong ID/Password".center(130))
