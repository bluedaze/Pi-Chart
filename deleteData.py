import sqlite3
from datetime import datetime, timedelta
from datetime import datetime, timedelta

today = datetime.today() 
yesterday = today - timedelta(hours=24)
print(yesterday)
today.strftime('%Y-%m-%d')
yesterday.strftime('%Y-%m-%d')
conn = sqlite3.connect("pidb.db", isolation_level=None)
conn.execute('pragma journal_mode=wal;')
c = conn.cursor()
c.execute("DELETE FROM tweets WHERE timeStamp LIKE (?)", (yesterday,))
conn.close()