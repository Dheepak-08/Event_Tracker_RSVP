import os
import sqlite3
import pymysql
from config import Config

class DatabaseManager:
    def __init__(self):
        self.use_mysql = False
        self.connection = None

    def get_connection(self):
        """Attempts MySQL connection, falls back to SQLite if MySQL is unavailable."""
        # Try MySQL first if credentials exist
        try:
            conn = pymysql.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DB,
                port=Config.MYSQL_PORT,
                cursorclass=pymysql.cursors.DictCursor,
                connect_timeout=2
            )
            self.use_mysql = True
            return conn
        except Exception as e:
            # Fallback to SQLite database for instant zero-dependency execution
            self.use_mysql = False
            conn = sqlite3.connect(Config.SQLITE_DB_PATH)
            conn.row_factory = sqlite3.Row
            return conn

    def init_db(self):
        """Initializes tables and seeds initial data."""
        conn = self.get_connection()
        cursor = conn.cursor()

        if self.use_mysql:
            # Execute schema in MySQL
            with open(os.path.join(Config.BASE_DIR, 'schema.sql'), 'r') as f:
                sql_statements = f.read().split(';')
                for stmt in sql_statements:
                    if stmt.strip():
                        cursor.execute(stmt)
            conn.commit()
        else:
            # Execute schema in SQLite
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS hosts (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'Event Host',
                department TEXT DEFAULT 'University Faculty',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                event_date TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                venue TEXT NOT NULL,
                capacity INTEGER NOT NULL DEFAULT 100,
                registered_count INTEGER DEFAULT 0,
                attended_count INTEGER DEFAULT 0,
                status TEXT DEFAULT 'Published',
                deadline TEXT NOT NULL,
                banner_url TEXT,
                host_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS registrations (
                id TEXT PRIMARY KEY,
                event_id TEXT NOT NULL,
                student_name TEXT NOT NULL,
                student_email TEXT NOT NULL,
                student_id TEXT NOT NULL,
                qr_code TEXT UNIQUE NOT NULL,
                registration_date TEXT NOT NULL,
                status TEXT DEFAULT 'Registered',
                scan_time TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
            conn.commit()

        # Seed initial data if database is empty
        self.seed_initial_data(conn)
        conn.close()

    def seed_initial_data(self, conn):
        cursor = conn.cursor()

        # Check if host exists
        if self.use_mysql:
            cursor.execute("SELECT COUNT(*) as count FROM hosts")
            count = cursor.fetchone()['count']
        else:
            cursor.execute("SELECT COUNT(*) as count FROM hosts")
            count = cursor.fetchone()[0]

        if count == 0:
            # 1. Seed Host
            cursor.execute(
                "INSERT INTO hosts (id, name, email, password_hash, role, department) VALUES (?, ?, ?, ?, ?, ?)" if not self.use_mysql else
                "INSERT INTO hosts (id, name, email, password_hash, role, department) VALUES (%s, %s, %s, %s, %s, %s)",
                ("host-1", "Prof. Alex Mercer", "host@campuspulse.edu", "password123", "Event Coordinator", "Computer Science & Engineering")
            )

            # 2. Seed Events
            events_data = [
                ("evt-101", "Python Full-Stack & AI Workshop", "Technical", 
                 "Hands-on intensive workshop covering Python backend development, REST APIs, and building modern AI-assisted web applications.",
                 "2026-09-15", "10:00", "16:00", "Auditorium Hall A, Tech Block", 100, 76, 52, "Published", "2026-09-14",
                 "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&auto=format&fit=crop&q=80", "host-1"),
                ("evt-102", "Campus Hackathon 2026", "Hackathon",
                 "24-hour annual coding sprint to solve real-world campus & sustainability challenges.",
                 "2026-10-01", "09:00", "09:00", "Main Innovation Lab", 150, 120, 0, "Published", "2026-09-28",
                 "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800&auto=format&fit=crop&q=80", "host-1"),
                ("evt-103", "Robotics & Automation Symposium", "Seminars",
                 "Keynote talks from industry leaders in autonomous robotics and smart systems.",
                 "2026-08-10", "11:00", "15:00", "Seminar Hall 2", 80, 80, 74, "Completed", "2026-08-08",
                 "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800&auto=format&fit=crop&q=80", "host-1")
            ]

            for evt in events_data:
                cursor.execute(
                    "INSERT INTO events (id, title, category, description, event_date, start_time, end_time, venue, capacity, registered_count, attended_count, status, deadline, banner_url, host_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)" if not self.use_mysql else
                    "INSERT INTO events (id, title, category, description, event_date, start_time, end_time, venue, capacity, registered_count, attended_count, status, deadline, banner_url, host_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    evt
                )

            # 3. Seed Registrations
            registrations_data = [
                ("reg-001", "evt-101", "Dheepak R", "dheepak.r@student.edu", "21CS042", "CP-QR-STU-1001", "2026-08-01 10:30", "Attended", "2026-09-15 09:45"),
                ("reg-002", "evt-101", "Dheepak Kumar", "dheepak.k@student.edu", "21CS043", "CP-QR-STU-1002", "2026-08-02 14:15", "Attended", "2026-09-15 09:50"),
                ("reg-003", "evt-101", "Anita Sharma", "anita.s@student.edu", "22EC018", "CP-QR-STU-1003", "2026-08-03 11:20", "Registered", None),
                ("reg-004", "evt-101", "Rahul Verma", "rahul.v@student.edu", "21ME089", "CP-QR-STU-1004", "2026-08-04 16:45", "Attended", "2026-09-15 09:55"),
                ("reg-005", "evt-101", "Priya Nair", "priya.n@student.edu", "22CS102", "CP-QR-STU-1005", "2026-08-05 09:10", "Registered", None),
                ("reg-006", "evt-102", "Karthik Raja", "karthik.r@student.edu", "21CS055", "CP-QR-STU-1006", "2026-08-06 12:00", "Registered", None),
                ("reg-007", "evt-102", "Dheepak R", "dheepak.r@student.edu", "21CS042", "CP-QR-STU-1007", "2026-08-07 15:30", "Registered", None)
            ]

            for reg in registrations_data:
                cursor.execute(
                    "INSERT INTO registrations (id, event_id, student_name, student_email, student_id, qr_code, registration_date, status, scan_time) VALUES (?,?,?,?,?,?,?,?,?)" if not self.use_mysql else
                    "INSERT INTO registrations (id, event_id, student_name, student_email, student_id, qr_code, registration_date, status, scan_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    reg
                )

            conn.commit()

db = DatabaseManager()
