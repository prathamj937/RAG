import sqlite3

connection = sqlite3.connect('chatbot.db')

cursor = connection.cursor()

table_info = """
CREATE TABLE Student(Name VARCHAR(50) NOT NULL,
Age INTEGER NOT NULL,Class VARCHAR(50) NOT NULL,
Subject VARCHAR(50) NOT NULL,Marks INTEGER NOT NULL)
 """

cursor.execute(table_info)

cursor.execute("INSERT INTO Student VALUES('John', 20, 'B.Tech', 'CSE', 85)")
cursor.execute("INSERT INTO Student VALUES('Alice', 22, 'B.Sc', 'Physics', 90)")
cursor.execute("INSERT INTO Student VALUES('Bob', 21, 'B.Com', 'Commerce', 75)")
cursor.execute("INSERT INTO Student VALUES('Eve', 23, 'B.A', 'English', 88)")

print("the inserted values are:")
data = cursor.execute("SELECT * FROM Student")

for row in data:
    print(row)

connection.commit()
connection.close()