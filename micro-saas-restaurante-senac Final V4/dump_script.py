import sqlite3

conn = sqlite3.connect('db.sqlite3')
with open('mysql_dump.sql', 'w') as f:
    for line in conn.iterdump():
        f.write(line + '\n')
conn.close()
