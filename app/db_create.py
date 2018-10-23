
from app import db, create_app
from app.task import init_config

app = create_app()
db.drop_all(app=app)
db.create_all(app=app)
init_config()

print('ssssssss')