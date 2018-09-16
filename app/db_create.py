from app import db, app

db.drop_all(app=app)
db.create_all(app=app)