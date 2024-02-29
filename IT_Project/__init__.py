import sqlite3
conn = sqlite3.connect('existing_database.db')

car = conn.cursor()
car.execute('''
        CREATE TABLE CAR(
 ID CHAR PRIMARY KEY     NOT NULL,
 MODEL          TEXT    NOT NULL,
 BRAND          TEXT,
 DEFINE         TEXT
);
    ''')
car.execute("INSERT INTO CAR (ID,MODEL,BRAND,DEFINE) VALUES (1,'SUV','BMW','GOOD')")
car.execute("INSERT INTO CAR (ID,MODEL,BRAND,DEFINE) VALUES (2,'SUV','BMW','GOOD')")
conn.commit()
conn.close()
