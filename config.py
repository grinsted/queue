from huey import Huey
from huey.backends.sqlite_backend import SqliteQueue, SqliteDataStore

queue = SqliteQueue("queue", "queue.db")
result_store = SqliteDataStore("results", "results.db")
huey = Huey(queue, result_store=result_store)
