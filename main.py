import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Person(BaseModel):
    id: int
    name: str
    age: int
    email: str


def init_db():
    conn = sqlite3.connect('database.db') 
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS person (
            id INTEGER PRIMARY KEY,  
            name TEXT,              
            age INTEGER,           
            email TEXT )''')
    conn.commit()  
    conn.close()   

init_db()

@app.get("/")  
def read_root():
    return "FastAPI!"

@app.post("/person/")  
def create_person(person: Person):
    try:
        conn = sqlite3.connect('database.db')  
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO person (id, name, age, email) VALUES (?, ?, ?, ?)
        ''', (person.id, person.name, person.age, person.email))
        conn.commit() 
        conn.close()  
        return person  
    except sqlite3.IntegrityError: 
        raise HTTPException(status_code=400, detail="Человек с этим ID уже существует.")
