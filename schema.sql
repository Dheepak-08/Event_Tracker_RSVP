-- CampusPulse Database Schema (MySQL & SQLite compatible)

CREATE TABLE IF NOT EXISTS hosts (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'Event Host',
    department VARCHAR(100) DEFAULT 'University Faculty',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS events (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    event_date DATE NOT NULL,
    start_time VARCHAR(20) NOT NULL,
    end_time VARCHAR(20) NOT NULL,
    venue VARCHAR(150) NOT NULL,
    capacity INT NOT NULL DEFAULT 100,
    registered_count INT DEFAULT 0,
    attended_count INT DEFAULT 0,
    status VARCHAR(30) DEFAULT 'Published',
    deadline DATE NOT NULL,
    banner_url TEXT,
    host_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (host_id) REFERENCES hosts(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS registrations (
    id VARCHAR(50) PRIMARY KEY,
    event_id VARCHAR(50) NOT NULL,
    student_name VARCHAR(100) NOT NULL,
    student_email VARCHAR(120) NOT NULL,
    student_id VARCHAR(50) NOT NULL,
    qr_code VARCHAR(100) UNIQUE NOT NULL,
    registration_date VARCHAR(50) NOT NULL,
    status VARCHAR(30) DEFAULT 'Registered',
    scan_time VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);
