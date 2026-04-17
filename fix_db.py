import database, models

# 1. Create the tables
models.Base.metadata.create_all(bind=database.engine)

db = next(database.get_db())

# 2. Check if User 1 exists, if not, create him
user = db.query(models.User).filter(models.User.id == 1).first()
if not user:
    new_user = models.User(
        id=1, 
        username="Student", 
        interests="Python", 
        skill_level="Beginner", 
        streak=1, 
        progress=0
    )
    db.add(new_user)
    db.commit()
    print("✅ User #1 created successfully!")
else:
    print("✅ User #1 already exists.")
