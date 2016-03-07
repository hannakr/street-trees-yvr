from app import db

class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    civicNumber = db.Column(db.Integer, unique=True)
    stdStreet = db.Column(db.String(255), index=True)
    stdStreetSorted = db.Column(db.String(255), index=True)
    neighbourhoodName = db.Column(db.String(255), index=True)
    trees = db.relationship('Tree', backref='location', lazy='dynamic')

    def __repr__(self):
        return '<House %r>' % (self.stdStreet)

class Tree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    treeID = db.Column(db.Integer, unique=True)
    cell = db.Column(db.Integer)
    onStreet = db.Column(db.String(255))
    onStreetBlock = db.Column(db.String(255))
    streetSideName = db.Column(db.String(255))
    assigned = db.Column(db.String(255))
    heightRangeID = db.Column(db.Integer)
    diameter = db.Column(db.Float)
    datePlanted = db.Column(db.String(255))
    plantArea = db.Column(db.String(255))
    rootBarrier = db.Column(db.String(255))
    curb = db.Column(db.String(255))
    cultivarName = db.Column(db.String(255))
    genusName = db.Column(db.String(255))
    speciesName = db.Column(db.String(255))
    commonName = db.Column(db.String(255))
    onCorner = db.Column(db.String(255))
    house = db.Column(db.Integer, db.ForeignKey('house.id'))

    def __repr__(self):
        return '<Tree %r>' % (self.commonName)
