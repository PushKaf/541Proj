#Project on Library Management System
#--------------------------------------------------------------------------------
#MODULE : LIBRARY MANAGEMENT
import Database
import Menulib
from rediStuff import create_index
from const import ISSUE_TABLE, ISSUE_SCHEMA

Database.DatabaseCreate()
Database.TablesCreate()

client = create_index(f"{ISSUE_TABLE}-idx", ISSUE_TABLE, ISSUE_SCHEMA)

while True:
    # time.sleep(5)
    # Book.clrscreen()
    print("\t\t\t Library Management\n")
    print("=====================================================================")
    print("1. Book Management")
    print("2. Members Management")
    print("3. Issue/Return Book")
    print("4. Exit")
    choice = int(input("Enter Choice between 1 to 4 -------> : "))
    if choice == 1:
        Menulib.Menubook()
    elif choice == 2:
        Menulib.MenuMember()
    elif choice == 3:
        Menulib.MenuIssueReturn(client)
    elif choice == 4:
        break
    else:
        print("Wrong Choice.....Enter Your Choice again")
        x = input("Press any key to continue")


