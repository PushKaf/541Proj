from redisearch import TextField


REDIS_HOST = "localhost"
REDIS_PORT = 6379

BOOK_RECORD_FN = 'book_records.csv'
MEMBER_FN = 'member_records.csv'
ISSUE_FN = 'issue_records.csv'

BOOK_RECORD_DATA_MAP = {
    "k_bno": (0, int),
    "bname": (1, str),
    "auth": (2, str),
    "price": (3, int),
    "publ": (4, str),
    "qty": (5, int),
    "date": (6, str)
}

MEMBER_DATA_MAP = {
    "k_mno": (0, int),
    "mname": (1, str),
    "date_of_membership": (2, str),
    "addr": (3, str),
    "mob": (4, str)
}

ISSUE_DATA_MAP = {
    "k_bno": (0, int),
    "mno": (1, int),
    "d_o_issue": (2, str),
    "d_o_ret": (3, str)
}

BOOK_RECORD_TABLE = "bookrecord"
BOOK_RECORD_SCHEMA = (
    TextField("bname", weight=5),
    TextField("author", weight=3)
)

MEMBER_TABLE = "member"
MEMBER_SCHEMA = (
    TextField("mname", weight=5),
)

ISSUE_TABLE = "issue"
ISSUE_SCHEMA = (
    TextField("mno", weight=5),
)

