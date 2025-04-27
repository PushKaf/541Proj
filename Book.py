#PYTHON MODULE: BOOK
import os
import platform
import redis
from const import REDIS_HOST, REDIS_PORT, BOOK_RECORD_TABLE


def clrscreen():
    if platform.system() == "Windows":
        print(os.system("cls"))


def _does_bno_exist(r, bno):
    table_key = f"{BOOK_RECORD_TABLE}:{bno}"

    if r.exists(table_key):
        return True
    
    return False

def insertData():
    r = redis.Redis(REDIS_HOST, REDIS_PORT, db=0, decode_responses=True)
    
    bno = input("Enter Book Code : ")
    table_key = f"{BOOK_RECORD_TABLE}:{bno}"

    if _does_bno_exist(r, bno):
        print(f"BNO: {bno} already exists in the table. Please Update if needed.")
        r.close()
        return

    bname = input("Enter Book Name : ")
    Auth = input("Enter Book Author's Name : ")
    price = int(input("Enter Book Price : "))
    publ = input("Enter Publisher of Book : ")
    qty = int(input("Enter Quantity purchased : "))
    
    print("Enter Date of Purchase (Date/Month and Year seperately) : ")
    DD = int(input("Enter Date : "))
    MM = int(input("Enter Month : "))
    YY = int(input("Enter Year : "))
    
    book_map = {
        "bname": bname,
        "auth": Auth,
        "price": price,
        "publ": publ,
        "qty": qty,
        "date": f"{DD}/{MM}/{YY}"
    }

    r.hset(table_key, mapping=book_map)
    print("Record Inserted.")

    r.close()


def deleteBook():
    r = redis.Redis(REDIS_HOST, REDIS_PORT, db=0, decode_responses=True)

    bno = input("Enter Book Code of Book to be deleted from the Library : ")
    table_key = f"{BOOK_RECORD_TABLE}:{bno}"
    
    if not _does_bno_exist(r, bno):
        print(f"BNO: {bno} dosent exist in the table. Please add if needed.")
        return
    
    if r.delete(table_key):
        print("Successfully deleted.")
    else:
        print("Something went wrong. Please try again.")

    r.close()


def SearchBookRec():
    r = redis.Redis(REDIS_HOST, REDIS_PORT, db=0, decode_responses=True)

    bno = input("Enter Book No to be Searched from the Library : ")
    table_key = f"{BOOK_RECORD_TABLE}:{bno}"
    
    if not _does_bno_exist(r, bno):
        print(f"BNO: {bno} dosent exist in the table. Please add if needed.")
        return

    book = r.hgetall(table_key)

    print("=============================================================")
    print("Book Code : ", bno)
    print("Book Name : ", book["bname"])
    print("Author of Book : ", book["auth"])
    print("Price of Book : ", book["price"])
    print("Publisher : ", book["publ"])
    print("Total Quantity in Hand : ", book["qty"])
    print("Purchased On : ", book["date"])
    print("=============================================================")

    r.close()

def UpdateBook():
    r = redis.Redis(REDIS_HOST, REDIS_PORT, db=0, decode_responses=True)
    
    bno = input("Enter Book Code (BNO) to Update: ")
    table_key = f"{BOOK_RECORD_TABLE}:{bno}"

    if not _does_bno_exist(r, bno):
        print(f"BNO: {bno} dosent exist in the table. Please add if needed.")
        r.close()
        return

    bname = input("Enter Book Name : ")
    Auth = input("Enter Book Author's Name : ")
    price = int(input("Enter Book Price : "))
    publ = input("Enter Publisher of Book : ")
    qty = int(input("Enter Quantity purchased : "))
    
    print("Enter Date of Purchase (Date/Month and Year seperately) : ")
    DD = int(input("Enter Date : "))
    MM = int(input("Enter Month : "))
    YY = int(input("Enter Year : "))
    
    book_map = {
        "bname": bname,
        "auth": Auth,
        "price": price,
        "publ": publ,
        "qty": qty,
        "date": f"{DD}/{MM}/{YY}"
    }

    r.hset(table_key, mapping=book_map)
    print("Record Updated.")

    r.close()