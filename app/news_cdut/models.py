from app import db


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

    # def set_origin_url(self, origin_url):
    #     self.origin_url = origin_url
    #
    # def get_origin_url(self):
    #     return self.origin_url
    #
    # def set_info(self, info):
    #     self.info = info
    #
    # def get_info(self):
    #     return self.info

