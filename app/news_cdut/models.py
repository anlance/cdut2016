from app import db


# 成都理工教务处消息
class NewsCdut(db.Model):
    __tablename__ = 'newscdut'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    origin_url = db.Column(db.String(200))
    info = db.Column(db.String(160))
    time = db.Column(db.Date)

    def __init__(self, origin_url, info, time):
        self.origin_url = origin_url
        self.info = info
        self.time = time

    def __repr__(self):
        return '<NewsCdut %r>' % self.info

