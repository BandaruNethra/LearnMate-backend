import sqlite3

# Data for 20 starter courses
starter_courses = [
    # PYTHON & DATA SCIENCE
    ("Python for Absolute Beginners", "Learn Python from scratch in this comprehensive course.", "kqtD5dpn9C8", "Python", "6h 14m"),
    ("Python Data Science Handbook", "Master Pandas, NumPy and Matplotlib.", "rfscVS0vtbw", "Data Science", "12h 00m"),
    ("Machine Learning with Python", "Build your first predictive models.", "GwIo3gDZCVQ", "AI/ML", "3h 00m"),
    
    # WEB DEVELOPMENT (Frontend)
    ("HTML & CSS Full Course", "The foundation of web development.", "ok-plXXHlWw", "Web Dev", "11h 00m"),
    ("JavaScript Mastery 2026", "Learn modern JS (ES6+) basics to advanced.", "W6NZfCO5SIk", "Web Dev", "6h 30m"),
    ("React.js Beginner to Pro", "Build dynamic user interfaces with React.", "LDB4uaJ87e0", "Web Dev", "2h 00m"),
    ("Tailwind CSS Crash Course", "Modern styling for the web.", "dFgzHOX84xQ", "Web Dev", "2h 15m"),
    ("Next.js 14 Full Course", "The future of React development.", "wm5gMKuwSYk", "Web Dev", "5h 00m"),

    # BACKEND & DATABASES
    ("SQL & Databases for Beginners", "Master relational database design.", "ztHopE5Wnpc", "Databases", "4h 00m"),
    ("Node.js & Express Course", "Build powerful backend APIs.", "Oe421EPjeBE", "Backend", "8h 00m"),
    ("PostgreSQL Tutorial", "Advanced database management.", "qw--VYLpxG4", "Databases", "4h 15m"),
    ("FastAPI Python Backend", "Modern, high-performance web APIs.", "tLKKmouUams", "Backend", "2h 30m"),

    # COMPUTER SCIENCE FOUNDATIONS
    ("Harvard CS50x 2026", "The gold standard for Computer Science.", "IDDmrKyB8vU", "CS Fundamentals", "24h 00m"),
    ("Data Structures & Algorithms", "Master the coding interview.", "8hly31RKIRg", "CS Fundamentals", "8h 00m"),
    ("Operating Systems Concepts", "How computers actually work.", "2m2iG4C96vM", "CS Fundamentals", "4h 00m"),

    # OTHER LANGUAGES
    ("C++ Full Course 2026", "Master system-level programming.", "vLnPwxZdW4Y", "Programming", "31h 00m"),
    ("Java Mastery in One Video", "The ultimate guide to Java.", "eIrMbAQSU34", "Programming", "9h 30m"),
    ("Rust Programming Basics", "The most loved language by developers.", "MsocrezY9n4", "Programming", "2h 00m"),
    ("Go (Golang) for Beginners", "Build scalable cloud software.", "un6ZyFkqFKo", "Programming", "6h 30m"),
    ("SwiftUI (iOS Development)", "Build iPhone apps from scratch.", "F2ojC6ZaZ6w", "Mobile", "3h 00m")

    # BACKEND MASTERY
    ("Docker & Kubernetes for Beginners", "Master containerization and cloud orchestration.", "pg19giVax6w", "Backend", "3h 45m"),
    ("Redis Crash Course", "Learn high-speed in-memory data caching.", "jgpVdJB2ne0", "Backend", "1h 20m"),
    ("System Design for Beginners", "How to design apps for millions of users.", "SqcXyztPa1o", "Backend", "2h 30m"),
    
    # ADVANCED PROGRAMMING
    ("Effective C# (C-Sharp) Mastery", "Build enterprise-grade apps with .NET.", "GhQdlIFylQ8", "Programming", "4h 15m"),
    ("PHP 8.3 & Laravel Bootcamp", "The most popular way to build web apps.", "376XnO_k8vI", "Programming", "7h 00m"),
    ("Functional Programming in Scala", "A different way to think about code.", "vMAtnN08XhI", "Programming", "3h 00m")
]

def seed_db():
    conn = sqlite3.connect('learnmate.db') # Ensure this matches your DB name
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            video_id TEXT,
            category TEXT,
            duration TEXT
        )
    ''')

    # Insert data
    cursor.executemany('''
        INSERT INTO courses (title, description, video_id, category, duration)
        VALUES (?, ?, ?, ?, ?)
    ''', starter_courses)
    
    conn.commit()
    conn.close()
    print("✅ Successfully added 20 courses to LearnMate!")

if __name__ == "__main__":
    seed_db()