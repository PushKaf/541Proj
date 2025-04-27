#PYTHON MODULE: ISSUE
from datetime import date
import redis
from const import REDIS_HOST, REDIS_PORT, ISSUE_TABLE
from rediStuff import search_by

def clrscreen():
    print('\n' * 5)

def _does_bno_exist(r, bno):
    table_key = f"{ISSUE_TABLE}:{bno}"

    if r.exists(table_key):
        return True
    
    return False

def SearchIssuedBooks(client):
    r = redis.Redis(REDIS_HOST, REDIS_PORT, db=0, decode_responses=True)

    mno = input("Enter Member No to search issued book : ")
    res = search_by(client, mno, search_type="mno")
    
    Rec_count = 0
    if res.total > 0:
        for issue in res.docs:
            
            data = issue.__dict__
            bno = issue.id.split(":")[-1]

            Rec_count += 1
            print("=============================================================")
            print("1.Book Code : ", bno)
            print("2.Member Code : ", data["mno"])
            print("3.Date of Issue : ", data["d_o_issue"])
            print("4.Date of Return : ", data["d_o_ret"])
            print("=============================================================")
            if Rec_count%2 == 0:
                input("Press any key continue")
                clrscreen()
                print(Rec_count, "Record(s) found")
    else:
        print(f"No Records for MNO: {mno} found.")
    
    r.close()


def issueBook():
    r = redis.Redis(REDIS_HOST, REDIS_PORT, db=0, decode_responses=True)

    bno = input("Enter Book Code to issue : ")
    table_key = f"{ISSUE_TABLE}:{bno}"

    if _does_bno_exist(r, bno):
        print("This book is already issued.")
        r.close()
        return

    mno = input("Enter Member Code : ")
    
    print("Enter Date Issue (Date/Month and Year separately) : ")
    DD = int(input("Enter Date : "))
    MM = int(input("Enter Month : "))
    YY = int(input("Enter Year : "))
    
    issue_map = {
        "mname": int(mno),
        "d_o_issue": f"{DD}/{MM}/{YY}",
        "d_o_ret": ""
    }

    r.hset(table_key, mapping=issue_map)

    print("Recorded Inserted.")
    r.close()


def returnBook():
    r = redis.Redis(REDIS_HOST, REDIS_PORT, db=0, decode_responses=True)

    bno = input("Enter Book Code of the Book to be returned to the Library : ")
    table_key = f"{ISSUE_TABLE}:{bno}"
    
    if not _does_bno_exist(bno):
        print("Book Isnt Issued.")
        r.close()
        return
    
    Mno = input("Enter Member Code of Member who is returning Book : ")
    retDate = date.today().strftime("%d/%m/%y")
    
    r.hset(table_key, "d_o_ret", retDate)

    print(f"Book ({bno}) for MNO: {Mno} returned.")
    r.close()