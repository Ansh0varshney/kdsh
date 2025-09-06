def get_all_papers():
    conn = sqlite3.connect('papers.db')
    c = conn.cursor()
    c.execute('SELECT id, content FROM papers')
    rows = c.fetchall()
    conn.close()
    return rows
# Simple SQLite database setup for storing papers and results
import sqlite3

def init_db():
    conn = sqlite3.connect('papers.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS papers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        content TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paper_id INTEGER,
        pipeline TEXT,
        result TEXT,
        FOREIGN KEY(paper_id) REFERENCES papers(id)
    )''')
    conn.commit()
    conn.close()

def add_paper(filename, content):
    conn = sqlite3.connect('papers.db')
    c = conn.cursor()
    c.execute('INSERT INTO papers (filename, content) VALUES (?, ?)', (filename, content))
    paper_id = c.lastrowid
    conn.commit()
    conn.close()
    return paper_id

def get_paper(paper_id):
    conn = sqlite3.connect('papers.db')
    c = conn.cursor()
    c.execute('SELECT content FROM papers WHERE id=?', (paper_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None
