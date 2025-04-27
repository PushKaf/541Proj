#PYTHON MODULE: MEMBER
import redis
from const import REDIS_HOST, REDIS_PORT, MEMBER_TABLE


def clrscreen():
    print('\n' * 5)

def _does_mno_exist(r, mno):
    table_key = f"{MEMBER_TABLE}:{mno}"

    if r.exists(table_key):
        return True
    
    return False

def insertMember():
    r = redis.Redis(REDIS_HOST, REDIS_PORT, db=0, decode_responses=True)
    
    mno = input("Enter Member Code : ")
    table_key = f"{MEMBER_TABLE}:{mno}"

    if _does_mno_exist(r, mno):
        print(f"MNO: {mno} already exists in the table. Please Update if needed.")
        r.close()
        return

    mname = input("Enter Member Name : ")
    print("Enter Date of Membership (Date/Month and Year) seperately) : ")
    
    DD = int(input("Enter Date : "))
    MM = int(input("Enter Month : "))
    YY = int(input("Enter Year : "))
    
    addr = input("Enter Member Address : ")
    mob = int(input("Enter Member Mobile No. : "))

    mem_map = {
        "mname": mname,
        "date_of_membership": f"{DD}/{MM}/{YY}",
        "addr": addr,
        "mob": mob
    }

    r.hset(table_key, mapping=mem_map)

    print("Record Inserted.")
    r.close()


def deleteMember():
    r = redis.Redis(REDIS_HOST, REDIS_PORT, db=0, decode_responses=True)

    mno = input("Enter Member Code to be deleted from the Library : ")
    table_key = f"{MEMBER_TABLE}:{mno}"

    if not _does_mno_exist(r, mno):
        print(f"MNO: {mno} dosent exist in the table. Please add if needed.")
        return
    
    if r.delete(table_key):
        print(f"Successfully deleted MNO: {mno}.")
    else:
        print("Something went wrong. Please try again.")

    r.close()


def SearchMember():
    r = redis.Redis(REDIS_HOST, REDIS_PORT, db=0, decode_responses=True)


    mnm = input("Enter Member No to be Searched from the Library : ")
    table_key = f"{MEMBER_TABLE}:{mnm}"

    if not _does_mno_exist(r, mnm):
        print(f"MNO: {mnm} dosent exist in the table. Please add if needed.")
        return

    member = r.hget(table_key)

    print("=============================================================")
    print("Member Code : ", mnm)
    print("Member Name : ", member["mname"])
    print("Date of Membership : ", member["date_of_membership"])
    print("Address : ", member["addr"])
    print("Mobile No. of Member : ", member["mob"])
    print("====================================]=========================")

    r.close()


def UpdateMember():
    r = redis.Redis(REDIS_HOST, REDIS_PORT, db=0, decode_responses=True)

    mno = input("Enter Member Code of Member to be Updated from the Library : ")
    table_key = f"{MEMBER_TABLE}:{mno}"

    if not _does_mno_exist(r, mno):
        print(f"MNO: {mno} dosent exist in the table. Please add if needed.")
        return

    print("Enter new data")
    mname = input("Enter Member Name : ")
    
    print("Enter Date of Membership (Date/Month and Year seperately) : ")
    DD = int(input("Enter Date : "))
    MM = int(input("Enter Month : "))
    YY = int(input("Enter Year : "))
    
    addr = input("Enter Member address : ")
    mob = input("Enter Member's mobile no : ")
    
    mem_map = {
        "mname": mname,
        "date_of_membership": f"{DD}/{MM}/{YY}",
        "addr": addr,
        "mob": mob
    }

    r.hset(table_key, mapping=mem_map)
    print(f"Member ({mno}) successfully updated.")

    r.close()

