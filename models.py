from flask_login import UserMixin
from extentions import db

# in this file all the tables in the database are setout and the password check is done for each table. user roles are also defined.
class customers(db.Model, UserMixin): # creates database table for customer accounts

    id = db.Column(db.Integer, primary_key = True)
    firstName = db.Column(db.String(255))
    lastName = db.Column(db.String(255))
    email = db.Column(db.String(255), unique = True)
    password = db.Column(db.String(255))
    address = db.Column(db.Integer)

    def setPassword(self, password):
        from extentions import bcrypt
        passwordHash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.password = passwordHash
    def checkPassword(self, password):
        from extentions import bcrypt
        if bcrypt.check_password_hash(self.password,password):
            return True
        else:
            return False

    @property
    def role(self):
        return "customer"


class farmers(db.Model, UserMixin):  #creates database table for farmer accounts

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(255))
    lastName = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    address = db.Column(db.Integer)
    description = db.Column(db.String(500))
    profilePicture= db.Column(db.String)

    # functions for setting farmer account values within the database
    def setPassword(self, password):
        from extentions import bcrypt
        passwordHash = bcrypt.generate_password_hash(password)
        self.password = passwordHash
    def checkPassword(self, password):
        from extentions import bcrypt
        if bcrypt.check_password_hash(self.password, password):
            return True
        else:
            return False

    @property
    def role(self):
        return "farmer"

class admins(db.Model, UserMixin): # creates database table for admin accounts

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(255))
    lastName = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    # functions for setting admin account values within the database
    def setPassword(self, password):
        from extentions import bcrypt
        passwordHash = bcrypt.generate_password_hash(password)
        self.password = passwordHash
    def checkPassword(self, password):
        from extentions import bcrypt
        if bcrypt.check_password_hash(self.password, password):
            return True
        else:
            return False

    @property
    def role(self):
        return "admin"
class drivers(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(255))
    lastName = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    profilePicture = db.Column(db.String)

    def SetPassword(self, passowrd):
        from extensions import bcrypt
        passwordHash = bcrypt.generate_password_hash(passowrd)
        self.password = passwordHash
    def CheckPassword(self, password):
        from extensions import bcrypt
        if bcrypt.check_password_hash(self.password, password):
            return True
        else:
            return False

    @property
    def role(self):
        return "driver"


class products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image = db.Column(db.String)
    farmer_id = db.Column(db.Integer, db.ForeignKey("farmers.id"))
    farmer = db.relationship("farmers", backref="products")
    price = db.Column(db.Numeric(8, 2))
    amount = db.Column(db.Integer)
    description = db.Column(db.String)
    active = db.Column(db.Boolean)
    expiry = db.Column(db.Date)

class orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    products = db.Column(db.String)
    finalCost = db.Column(db.Numeric(8,2))
    delivery = db.Column(db.String)
    pickup = db.Column(db.String)


