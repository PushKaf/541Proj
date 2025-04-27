"""CREATING DATABASES AND ALL THE REQUIRED TABLES NEEDED TO RUN THE PROJECT
DATABASE NAME: Library
TABLES: Bookrecord, Member, Issue"""

from rediStuff import create_index
from const import ISSUE_TABLE, ISSUE_SCHEMA, BOOK_RECORD_TABLE, BOOK_RECORD_SCHEMA, MEMBER_TABLE, MEMBER_SCHEMA


def DatabaseCreate():
    print("No need to create a database.")


def TablesCreate():
    print("No need to create tables.")

bkr_client = create_index(f"{BOOK_RECORD_TABLE}-idx", BOOK_RECORD_TABLE, BOOK_RECORD_SCHEMA)
issue_client = create_index(f"{ISSUE_TABLE}-idx", ISSUE_TABLE, ISSUE_SCHEMA)
member_client = create_index(f"{MEMBER_TABLE}-idx", MEMBER_TABLE, MEMBER_SCHEMA)