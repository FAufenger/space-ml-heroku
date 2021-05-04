def create_classes(db):
    class StarDecipher(db.Model):
        __tablename__ = 'star_decipher'

        id = db.Column(db.Integer, primary_key=True)
        Temperature = db.Column(db.Integer)
        R = db.Column(db.Integer)
        L = db.Column(db.Integer)
        AM = db.Column(db.Integer)
        Color = db.Column(db.Integer)
        Spectral_Class = db.Column(db.Integer)

        def __repr__(self):
            return '<StarDecipher %r>' % (self.name)
    return StarDecipher
