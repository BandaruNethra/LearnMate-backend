import models
from database import SessionLocal, engine

# Create the database tables
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Check if the test user already exists
existing_user = db.query(models.User).filter(models.User.id == 1).first()

if not existing_user:
    # Create a dummy student for testing
    test_user = models.User(
        id=1,
        username="student_one",
        interests='["Python", "Robotics"]', # JSON string
        skill_level="Beginner",
        streak=3
    )
    db.add(test_user)
    db.commit()
    print("✅ Success! Test user 'student_one' added to learnmate.db")
else:
    print("ℹ️ Test user already exists.")

db.close()
