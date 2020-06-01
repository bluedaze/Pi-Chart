import sqlite3



def query_bracket(market):
	''' Query database for tweet markets '''
	conn = sqlite3.connect("pidb.db", isolation_level=None)
	conn.row_factory = sqlite3.Row
	c = conn.cursor()
	c.execute("SELECT bracket, buyYes, timeStamp FROM tweets WHERE marketName = ? ORDER BY bracket, timeStamp;", ( market,))
	selected = [tuple(row) for row in c.fetchall()]
	bracketData = {}
	for i in range(9):
		bracket = "B"+str(i+1)
		prices = [(item[1]) for item in selected if item[0] == bracket]
		timeStamp = [(item[2]) for item in selected if item[0] == bracket]
		bracketData[bracket] = prices, timeStamp
	c.close()
	conn.close()
	return bracketData

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