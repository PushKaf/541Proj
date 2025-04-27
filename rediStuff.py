import redis
from redisearch import Client, IndexDefinition, Query
import time
import csv
from const import *
from generator import *


BATCH_SIZE = 10000

def update_records(r, fn, tb_name, field_map, batch_size=BATCH_SIZE): 
    print(f"Uploading {fn} to {tb_name}...")
    unparsed_key = next((k for k in field_map if k.startswith("k_")), None)

    if not unparsed_key:
        print("No Key Found.")
        return
    
    key_idx = field_map[unparsed_key][0]
    pipe = r.pipeline()

    count = 0
    with open(fn, "r", encoding="utf-8") as fin:
        reader = csv.reader(fin)
        next(reader)

        for row in reader:
            key_name = f"{tb_name}:{row[key_idx]}"
            
            mapping = {}
            for field_name, (idx, field_type) in field_map.items():
                if field_name == unparsed_key:
                    continue

                raw = row[idx]
                try: 
                    mapping[field_name] = field_type(raw)
                except Exception as e:
                    print("Error converting into given type:", idx, field_type, field_name)

            pipe.hset(key_name, mapping=mapping)
            count+=1

            if count % batch_size == 0:
                pipe.execute()

    if pipe.command_stack:
        pipe.execute()

    print(f"Fully uploaded {fn} to {tb_name}.")

def create_index(index_name, table_name, schema):
    client = Client(index_name)
    idx_def = IndexDefinition(prefix=[table_name+":"])

    try:
        client.info()
        print("Index Already Created.")
    except redis.ResponseError:
        print(f"Creating Index: {index_name} for table: {table_name} w/ schema: {schema}")
        client.create_index(schema, definition=idx_def) 

    return client

def search_by(client, search_for, search_type="author"):
    res = client.search(Query(f"@{search_type}:{search_for}"))

    return res

# ---------------------- Benchmark stuff below ----------------------------
def benchmark(title, iterations, func, keys=None, *args, **kwargs):
    times = []

    for i in range(iterations):
        # Fresh conn & warmupppppp
        r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, socket_connect_timeout=30)
        r.ping()

        if keys:
            k = keys[i]
            start = time.perf_counter()
            func(r=r, keys=k)
            times.append(time.perf_counter() - start)

        else:
            start = time.perf_counter()
            func(r=r, *args, **kwargs)
            times.append(time.perf_counter() - start)

    print(f"{title}: {sum(times)/len(times)}s | Min: {min(times)} | Max: {max(times)}")

def time_keys(r, key_name):
    keys = r.keys(key_name) # Blocks the server
    for key in keys:
        record = r.hgetall(key)

def time_keys_iter(r, key_name):
    for key in r.scan_iter(key_name): # Dosent block server, only rets few results at a time, so server can stay responsive
        record = r.hgetall(key)

def time_pipeline(r, key_name, batch_size=BATCH_SIZE):
    pipe = r.pipeline() # Batches requests (reduces network latencies), atomic

    count = 0
    for key in r.scan_iter(key_name, count=BATCH_SIZE):
        pipe.hgetall(key)
        count+=1

        if count % batch_size == 0:
            pipe.execute() # runs the get all here
            pipe = r.pipeline()

    if pipe.command_stack:
        pipe.execute()

def time_pipeline_random(r, keys):
    pipe = r.pipeline()

    for k in keys:
        pipe.hgetall(k)

    res = pipe.execute()

def time_one(r, keys):
    res = r.hgetall(keys)

def bench_stan(iter, table_name):
    keys = [f"{table_name}:{random.randint(1, 500_000)}" for _ in range(iter)]
    benchmark(f"{table_name} Table: 1 Key", iter, time_one, keys=keys)

    keys = [[f"{table_name}:{random.randint(1, 500_000)}" for _ in range(1000)] for _ in range(iter)]
    benchmark(f"{table_name} Table: Random 1k Keys", iter, time_pipeline_random, keys=keys)



# --------------- Bench Stuff Above ------------------------


if __name__ == "__main__":
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, socket_connect_timeout=30)
    
    r.flushall()
    # print("Finished deleted all data\n")

    fns = set(os.listdir())

    if BOOK_RECORD_FN not in fns:
        bkr_fn = gen_book_records()

    benchmark("Book Record Table", 1, update_records, fn=BOOK_RECORD_FN, tb_name=BOOK_RECORD_TABLE, field_map=BOOK_RECORD_DATA_MAP)

    if ISSUE_FN not in fns:
        issue_fn = gen_issue_records()

    benchmark("Issue Record Table", 1, update_records, fn=ISSUE_FN, tb_name=ISSUE_TABLE, field_map=ISSUE_DATA_MAP)

    if MEMBER_FN not in fns:
        mem_fn = gen_member_records()

    benchmark("Member Record Table", 1, update_records, fn=MEMBER_FN, tb_name=MEMBER_TABLE, field_map=MEMBER_DATA_MAP)

    print ("Finished Generating & Updating Records.")

    bkr = f"{BOOK_RECORD_TABLE}:*"
    iss = f"{ISSUE_TABLE}:*"
    mem = f"{MEMBER_TABLE}:*"

    # benchmark("Blocking .keys() Approach", 3, time_keys, key_name=bkr)
    # benchmark("Nonblocking .scan_iter() Approach", 3, time_keys_iter, key_name=bkr)
    # benchmark("Pipeline Approach", 3, time_pipeline, key_name=bkr)


    # benchmark("Book Record Pipeline Approach", 1, time_pipeline, key_name=bkr)
    # benchmark("Issue Pipeline Approach", 1, time_pipeline, key_name=iss)
    # benchmark("Member Pipeline Approach", 1, time_pipeline, key_name=mem)


    bench_stan(10, BOOK_RECORD_TABLE)
    bench_stan(10, ISSUE_TABLE)
    bench_stan(10, MEMBER_TABLE)

