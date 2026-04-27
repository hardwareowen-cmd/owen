from main import app
from extentions import db
from models import farmers, products



with app.app_context():
    db.drop_all()
    db.create_all()

with app.app_context():
    products.__table__.drop(db.engine, checkfirst=True)
    products.__table__.create(db.engine)