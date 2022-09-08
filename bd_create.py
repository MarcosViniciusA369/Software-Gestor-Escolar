import sqlite3

conn = sqlite3.connect('banco_dados/Pyedu_bd.db')
cursor = conn.cursor()

def create_student():
    new_table = ("""CREATE TABLE IF NOT EXISTS student(
	RA INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"name_resp"	TEXT,
	"cpf" TEXT NOT NULL,
	"phone_number" TEXT,
	"birth_date" DATE,
	PRIMARY KEY("RA" AUTOINCREMENT)
);""")
    cursor.execute(new_table)
    conn.commit()

def create_teacher():
    new_table = ("""CREATE TABLE IF NOT EXISTS teacher(
    	id INTEGER NOT NULL,
    	"name"	TEXT NOT NULL,
    	"cpf" TEXT NOT NULL,
    	"phone_number" TEXT,
    	"birth_date" DATE
    );""")
    cursor.execute(new_table)
    conn.commit()

def create_subjects():
    new_table = ("""CREATE TABLE IF NOT EXISTS subjects(
    	id INTEGER NOT NULL,
    	"name"	TEXT NOT NULL,
    	id_teacher INTEGER,
    	FOREIGN KEY("id_teacher") REFERENCES "teacher"("id")
    );""")
    cursor.execute(new_table)
    conn.commit()

def create_class():
    new_table = ("""CREATE TABLE IF NOT EXISTS class(
	    "id" INTEGER NOT NULL,
	    "nome" TEXT NOT NULL,
	    "id_teacher" INTEGER,
	    PRIMARY KEY("id" AUTOINCREMENT),
	    FOREIGN KEY("id_teacher") REFERENCES "teacher"("id")
    );""")
    cursor.execute(new_table)
    conn.commit()

def create_grades():
    new_table = ("""CREATE TABLE IF NOT EXISTS grades(
	    "id" INTEGER NOT NULL,
	    "id_student" INTEGER NOT NULL,
	    "id_class" INTEGER,
	    "g1" REAL,
	    "g2" REAL,
	    "g3" REAL,
	    FOREIGN KEY("id_class") REFERENCES "class"("id"),
	    FOREIGN KEY("id_student") REFERENCES "student"("RA")
    );""")
    cursor.execute(new_table)
    conn.commit()

'''create_student()
create_teacher()
create_subjects()
create_grades()'''