
from app import db, create_app


app = create_app()
db.drop_all(app=app)
db.create_all(app=app)


print('ssssssss')