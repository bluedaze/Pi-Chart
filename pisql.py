import sqlite3


def query_bracket(bracket, market):
	''' Query database for tweet markets '''

	conn = sqlite3.connect("pidb.db", isolation_level=None)
	c = conn.cursor()
	
	selected = [(bracket[0], bracket[1]) for bracket in c.execute("SELECT buyYes, timeStamp, marketName from tweets WHERE bracket=? AND marketName=?", (bracket, market,))]	
	c.close()
	conn.close()
	return selected

def fetch_tables():
	tables = []
	''' Gets the names of all markets '''
	conn = sqlite3.connect("pidb.db", isolation_level=None)
	c = conn.cursor()
	c.execute("SELECT DISTINCT marketName FROM tweets")
	selected = c.fetchall()

	for item in selected:
	    tables.append(item[0])

	c.close()
	conn.close()

	return tables