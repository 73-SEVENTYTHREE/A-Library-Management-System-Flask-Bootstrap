from app import db

book_card=db.Table('book_card',
                   db.Column('book_number',db.String(20),db.ForeignKey('book.number'),primary_key=True),
                   db.Column('card_number',db.String(20),db.ForeignKey('card.number'),primary_key=True)
                   )

class Book(db.Model):
    __tablename__='book'
    number=db.Column(db.String(20),primary_key=True)
    type=db.Column(db.String(10))
    name=db.Column(db.String(10))
    publisher=db.Column(db.String(20))
    year=db.Column(db.Integer)
    author=db.Column(db.String(10))
    price=db.Column(db.DECIMAL(10,2))
    total=db.Column(db.Integer)
    stock=db.Column(db.Integer)
    card = db.relationship('Card', secondary=book_card,backref='borrowed_book')

class Card(db.Model):
    __tablename__='card'
    number=db.Column(db.String(20),primary_key=True)
    name=db.Column(db.String(10))
    department=db.Column(db.String(10))
    type=db.Column(db.String(10))

class Borecord(db.Model):
    __tablename__='borecord'
    ID=db.Column(db.Integer,autoincrement=True,primary_key=True,nullable=False)
    book_number = db.Column(db.String(10))
    card_number=db.Column(db.String(20))
    borrow_date=db.Column(db.Date)
    return_date=db.Column(db.Date)
    dealer=db.Column(db.String(10))
    __mapper_args__={
        "order_by":-return_date
    }

class Admin(db.Model):
    ID=db.Column(db.String(10),primary_key=True)
    pwd=db.Column(db.String(20))
    name=db.Column(db.String(10))
    email=db.Column(db.String(20))