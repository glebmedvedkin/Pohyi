import os
import sqlite3
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'files.db')

class FileIndexDB:
    def __init__(self, db_path=DB_PATH):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_index (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT UNIQUE,
                filename TEXT,
                size INTEGER,
                last_modified REAL
            )
        ''')
        self.conn.commit()

    def update_file(self, path):
        if not os.path.exists(path) or os.path.isdir(path):
            return
        
        filename = os.path.basename(path)
        size = os.path.getsize(path)
        last_modified = os.path.getmtime(path)

        self.cursor.execute('''
            INSERT INTO file_index (path, filename, size, last_modified)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(path) DO UPDATE SET
                size=excluded.size,
                last_modified=excluded.last_modified
        ''', (path, filename, size, last_modified))
        self.conn.commit()

    def remove_file(self, path):
        self.cursor.execute('DELETE FROM file_index WHERE path = ?', (path,))
        self.conn.commit()

class PohyiFileHandler(FileSystemEventHandler):
    def __init__(self, db: FileIndexDB):
        self.db = db
        super().__init__()

    def on_created(self, event):
        if not event.is_directory:
            print(f"[File] Created: {event.src_path}")
            self.db.update_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            print(f"[File] Modified: {event.src_path}")
            self.db.update_file(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"[File] Deleted: {event.src_path}")
            self.db.remove_file(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            print(f"[File] Moved: {event.src_path} -> {event.dest_path}")
            self.db.remove_file(event.src_path)
            self.db.update_file(event.dest_path)

def start_file_monitor(path_to_watch: str):
    print(f"Starting file monitor on: {path_to_watch}")
    db = FileIndexDB()
    
    # Initial scan
    print("Performing initial index scan...")
    for root, dirs, files in os.walk(path_to_watch):
        for file in files:
            db.update_file(os.path.join(root, file))
    print("Initial scan complete.")

    event_handler = PohyiFileHandler(db)
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=True)
    observer.start()
    return observer
