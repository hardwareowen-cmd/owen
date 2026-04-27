from models import customers, farmers, admins, drivers, products, orders
from extentions import db
from flask_login import login_user, current_user
from flask import flash, session, current_app
from werkzeug.utils import secure_filename
from decimal import Decimal
import os
import uuid


# the function behind the sign-up page.
# it checks each table for the email being used and then makes the account in the customers table it is not
# tells the user email already in use if it is
def signupfunc(firstName, lastName, email, password, address):
    customer = customers.query.filter_by(email=email).first()
    farmer = farmers.query.filter_by(email=email).first()
    admin = admins.query.filter_by(email=email).first()
    driver = drivers.query.filter_by(email=email).first()
    if customer or farmer or admin or driver:
        return False
    else:

        newCustomer = customers(firstName= firstName, lastName= lastName, email=email, address=address)
        newCustomer.setPassword(password)
        db.session.add(newCustomer)
        db.session.commit()
        return True


# checks each table for the email, then checks the password matches if so it logs the user in if not then it tells them their information is incorrect
def loginfunc(email,password,remember):
    user = None

    for table in [customers, farmers, admins, drivers]:
        u = table.query.filter_by(email=email).first()
        if u and u.checkPassword(password):
            user = u
            break

    if user:
        login_user(user, remember=remember)
        session['user_type'] = current_user.role
        return current_user.role
    else:
        flash("Check login details and try again")
        return False

# Function that was used to add the first admin account
def addAdmin():
    newAdmin = admins(firstName="admin", lastName="admin", email="admin@example.com")
    newAdmin.setPassword("password123")
    db.session.add(newAdmin)
    db.session.commit()

# the function behind the addNewAdmin page.
# it checks each table for the email being used and then makes the account in the admins table it is not
# tells the user email already in use if it is
def addNewAdmin(firstName, lastName, email, password):
    customer = customers.query.filter_by(email=email).first()
    farmer = farmers.query.filter_by(email=email).first()
    admin = admins.query.filter_by(email=email).first()
    driver = drivers.query.filter_by(email=email).first()
    if customer or farmer or admin or driver:
        return False
    else:
        newAdmin = admins(firstName=firstName, lastName=lastName, email=email)
        newAdmin.setPassword(password)
        db.session.add(newAdmin)
        db.session.commit()
        return True

# the function behind the addNewFarmer page.
# it checks each table for the email being used and then makes the account in the farmers table it is not
# tells the user email already in use if it is
def addNewFarmer(firstName, lastName, email, password, address, description, profilePicture):
    customer = customers.query.filter_by(email=email).first()
    farmer = farmers.query.filter_by(email=email).first()
    admin = admins.query.filter_by(email=email).first()
    driver = drivers.query.filter_by(email=email).first()
    profilePictureFolder = "/static/profilePictures"
    if customer or farmer or admin or driver:
        return False
    else:
        if profilePicture:
            folder = os.path.join(current_app.root_path, "static/profilePictures")
            os.makedirs(folder, exist_ok=True)
            filename = f"{uuid.uuid4()}_{secure_filename(profilePicture.filename)}"
            filepath = os.path.join(folder, filename)
            profilePicture.save(filepath)
            profilePath = f"static/profilePictures/{filename}"
            newFarmer = farmers(firstName=firstName, lastName=lastName, email=email, address=address, description=description,profilePicture=profilePath)
            newFarmer.setPassword(password)
            db.session.add(newFarmer)
            db.session.commit()
            return True

# the function behind the addNewDriver page.
# it checks each table for the email being used and then makes the account in the drivers table it is not
# tells the user email already in use if it is
def addNewDriver(firstName, lastName, email, password, profilePicture):
    customer = customers.query.filter_by(email=email).first()
    farmer = farmers.query.filter_by(email=email).first()
    admin = admins.query.filter_by(email=email).first()
    driver = drivers.query.filter_by(email=email).first()
    profilePictureFolder = "/static/profilePictures"
    if customer or farmer or admin or driver:
        return False
    else:
        if profilePicture:
            folder = os.path.join(current_app.root_path, "static/profilePictures")
            os.makedirs(folder, exist_ok=True)
            filename = f"{uuid.uuid4()}_{secure_filename(profilePicture.filename)}"
            filepath = os.path.join(folder, filename)
            profilePicture.save(filepath)
            profilePath = f"static/profilePictures/{filename}"
            newDriver = drivers(firstName=firstName, lastName=lastName, email=email, profilePicture=profilePath)
            newDriver.setPassword(password)
            db.session.add(newDriver)
            db.session.commit()
            return True

# the function behind the addNewProduct page.
# takes the product information and adds it to the products table
def addNewProduct(name, image, price, amount, description, active, expiry):
    if image:
        folder = os.path.join(current_app.root_path, "static/productPictures")
        os.makedirs(folder, exist_ok=True)
        filename = f"{uuid.uuid4()}_{secure_filename(image.filename)}"
        filepath = os.path.join(folder, filename)
        image.save(filepath)
        imagePath = f"productPictures/{filename}"
        newProduct = products(name=name, image=imagePath, price=price, amount=amount, description=description, active=active, expiry=expiry, farmer_id=current_user.id)
        db.session.add(newProduct)
        db.session.commit()
        return True

# adds item to the existing cart if it does exist or creates a new one and adds the item to the cart if not
def addItemToCart(item, quantity):
    cart = session.get("cart", [])

    if not isinstance(cart, list):
        cart = []

    print(cart)

    cart.append({"item": item, "quantity": quantity})
    session["cart"] = cart

# adds order information to the orders table
def order(method):
    order_items = []
    cart = session.get("cart", [])
    for item in cart:
        product = products.query.filter_by(id=item["item"]).first()
        item_info = f"{product.id},{product.name},{product.price},{item['quantity']}"
        order_items.append(item_info)
        print(order_items)
    if method == "delivery":

        neworder = orders(customer_id=current_user.id, products=str(order_items), delivery=current_user.address, pickup="none")
        db.session.add(neworder)
        db.session.commit()
        session["cart"] = []
        return flash("Order Placed For Delivery")
    elif method == "collection":
        neworder = orders(customer_id=current_user.id, products=str(order_items), delivery=current_user.address,pickup="none")
        db.session.add(neworder)
        db.session.commit()
        session["cart"] = []
        return flash("Order Placed for collection")
    else:
        return flash("an error occured")



