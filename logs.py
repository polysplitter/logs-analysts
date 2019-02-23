import psycopg2

db = psycopg2.connect("dbname=news")

c = db.cursor()

c.execute('select title from articles;')
all = c.fetchall()
print(all)
db.close()
