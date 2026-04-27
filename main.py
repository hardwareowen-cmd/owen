from flask import Flask, render_template, flash, redirect, url_for, session, request
from Bootstrap import Bootstrap5
from flask_login import login_required, current_user, LoginManager, login_user, logout_user
from extentions import db, bcrypt
from wrapper import role_required
from models import customers, farmers, admins, drivers, products
import forms
import functions


#flask setup
app = Flask(__name__)
app.secret_key = "SECRET KEY PLACEHOLDER"

#database setup
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

#bootstrao setup
bootstrap = Bootstrap5(app)
#bycrypt setup
bcrypt.init_app(app)

#login  manager setup
login_manager = LoginManager()
login_manager.init_app(app)

# this was used to add the first admin account
# with app.app_context():
#     functions.addAdmin()


#the user loader for the website. Loads the user id and user type to determind where to first send the user.
@login_manager.user_loader
def load_user(user_id):
    user_type = session.get("user_type")

    if user_type == "customer":
        return db.session.get(customers, int(user_id))
    elif user_type == "farmer":
        return db.session.get(farmers, int(user_id))
    elif user_type == "admin":
        return db.session.get(admins, int(user_id))
    elif user_type == "driver":
        return db.session.get(drivers, int(user_id))

    return None


#create the route for the Home page and displays the html file for it
@app.route("/")
def home():
    print("HELLO")
    return render_template("index.html")


#creates the route for the About Us page and displays the html file for it
@app.route("/aboutUs")
def aboutUs():
    return render_template("aboutUs.html")


#creates the route for the our farmers page and displays the html for it. Also pulls farmers details from the database and feeds it to the front-end
@app.route("/ourFarmers")
def ourFarmers():
    farmersData = farmers.query.all()
    return render_template("ourFarmers.html", farmersData=farmersData)


#creates the route for the login page and displays the html file for it. Also links to the loginfunc function which is in functions.py
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = forms.login() # pulls login form from forms.py
    if form.validate_on_submit(): #checks if form is validated
        email = form.email.data
        password = form.password.data
        remember = form.remember.data
        loginUser = functions.loginfunc(email, password, remember)

        #redrecting the user to the correct page depending on their user type
        if loginUser == "customer":
            return redirect(url_for('ourProducts'))
        elif loginUser == "farmer":
            return redirect('/farmerDashboard')
        elif loginUser == "admin":
            return redirect("/adminDashboard")
        elif loginUser == "driver":
            return redirect(redirect(url_for('driversJobs')))

    return render_template("login.html", form=form)


#creates the route for the Sign-Up page and displays the html file for it. Also links to the signupfunc function which is in functions.py
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = forms.signup()  #pulls sign up form from forms.py
    if form.validate_on_submit():
        firstname = form.firstName.data
        lastname = form.lastName.data
        email = form.email.data
        password = form.password.data
        address = form.address.data

        #calling the function and checking that the account is created before displaying a message determinding if the account was created or if the email is already in use
        if functions.signupfunc(firstname, lastname, email, password, address):
            flash("Account Created Successfully")
        else:
            flash("Email already in use.")
            return redirect("/signup")
    return render_template("signup.html",form=form)


#creates the route for the Our Products page and displays the html file for it. Requires user to be a customer to access
@app.route("/ourProducts")
@role_required("customer")
def ourProducts():
    Products = products.query.all()
    return render_template("ourProducts.html", Products=Products)


#creates the route for order history page. This isnt functional yet
@app.route("/orderHistory")
def orderHistory():
    return render_template("orderHistory.html")


#creates the route for the Your Products page and displays the html file for it. Also pulls data on products from the database. Requires user to be signed in to a farmers account to access.
@app.route("/yourProducts")
def yourProducts():
    Products = products.query.all()
    return render_template("yourProducts.html", Products=Products)


# Creates the route for the add products page and displays the html file for it.
# Also links to the addNewProducts function which is in functions.py.
# Pulls form from forms.py.
# Requires user to be signed in to a farmers account to access.
@app.route("/addProduct", methods=["GET", "POST"])
@role_required("farmer")
def addProducts():
    form = forms.addNewProduct()
    if form.validate_on_submit():
        name = form.name.data
        image = form.image.data
        price = form.price.data
        amount = form.amount.data
        description = form.description.data
        active = form.active.data
        expiry = form.expiry.data
        if functions.addNewProduct(name, image, price, amount, description, active, expiry):
            flash("Product Created Successfully")

    return render_template("addNewProduct.html", form=form)


#creates the route for the change product details page and displays the html file for it. This isn't functional yet
@app.route("/changeProductDetails")
def changeProductDetails():
    return render_template("changeProductDetails.html")


#creates the route for the current orders page and displays the html file for it. This isn't functional yet
@app.route("/currentOrders")
def currentOrders():
    return render_template("currentOrders.html")


#creates the route for the farmers dashboard page and displays the html file for it. Requires user to be signed in to a farmers account.
@app.route("/farmerDashboard")
@role_required("farmer")
def farmerDashboard():
    return render_template("farmerDashboard.html")


#creates the route for the admins dashboard page and displays the html file for it. Requires user to be signed in to an admins account.
@app.route("/adminDashboard")
@role_required("admin")
def adminDashboard():
    return render_template("adminDashboard.html")


#creates the route for the drivers jobs and displays the html file for it. This isnt functional yet
@app.route("/driversJobs")
def driversJobs():
    return render_template("driversJobs.html")

# used as a redirect point to log users and and send them to the home page
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

# creates the route for the addNewAccount page and displays the html for it.
@app.route("/addNewAccount", methods=['GET','POST'])
@role_required("admin")
def addNewAccount():
    return render_template("addNewAccount.html")

# creates the route for the addAdmin page and displays the html for it.
# pulls addNewAdmin form from forms.py
# requires user to be an admin
@app.route("/addAdmin", methods=['GET','POST'])
@role_required("admin")
def addAdmin():
    form = forms.addNewAdmin()
    if form.validate_on_submit():
        firstName = form.firstName.data
        lastName = form.lastName.data
        email = form.email.data
        password = form.password.data

        if functions.addNewAdmin(firstName, lastName, email, password):
            flash("Account Created Successfully")
        else:
            flash("Email already in use.")
            return redirect("/addAdmin")
    return render_template("addAdmin.html", form=form)

# creates the route for the addFarmer page and displays the html for it.
# pulls addNewFarmer form from forms.py
# requires user to be an admin
@app.route("/addFarmer", methods=["GET", "POST"])
@role_required("admin")
def addFarmer():
    form = forms.addNewFarmer()
    if form.validate_on_submit():
        firstName = form.firstName.data
        lastName = form.lastName.data
        email = form.email.data
        password = form.password.data
        address = form.address.data
        description = form.description.data
        profilePicture = form.profilepicture.data
        print(profilePicture)
        if functions.addNewFarmer(firstName, lastName, email, password, address, description, profilePicture):
            flash("Account Created Successfully")
        else:
            flash("Email already in use.")
            return redirect("/addFarmer")
    return render_template("addFarmer.html", form=form)

# creates the route for the addDriver page and displays the html for it.
# pulls addNewDriver form from forms.py
# requires user to be an admin

@app.route("/addDriver", methods=["GET", "POST"])
@role_required("admin")
def addDriver():
    form = forms.addNewDriver()
    if form.validate_on_submit():
        firstName = form.firstName.data
        lastName = form.lastName.data
        email = form.email.data
        password = form.password.data
        profilePicture = form.profilepicture.data
        if functions.addNewFarmer(firstName, lastName, email, password, profilePicture):
            flash("Account Created Successfully")
        else:
            flash("Email already in use.")
            return redirect("/addDriver")
    return render_template("addDriver.html", form=form)

# Creates the route for the cart page
# Pulls the cart data from the current user session
# pulls the product info as not all is stored in the cart
@app.route("/cart")
@role_required("customer")
def cart():
    cart = session.get("cart", [])
    Products = products.query.all()
    return render_template("cart.html", cart=cart, products=Products)

# the url redirected to by button on the ourProducts page that adds them to the cart
# gets the information from the html on which button is pressed then calls on the addItemToCart Function in functions.py
@app.route("/addToCart", methods=["POST"])
def addToCart():
    product_id = request.form.get('product_id')
    quantity = request.form.get('quantity')
    if not product_id:
        return redirect(request.referrer or url_for('ourProducts'))
    functions.addItemToCart(product_id, quantity )
    return redirect(request.referrer or url_for('ourProducts'))

# creates the route for the Orderpage
# allows customers to choose between delivery and collection
@app.route("/order")
def order():
    return render_template("order.html")

# gets the collection or delivery info and creates the order by calling the order function from functons.py
@app.route("/CompleteOrder", methods=["POST"])
def CompleteOrder():
    method = request.form.get("method")
    print(method)

    if method in ["delivery", "collection"]:
        functions.order(method)

# creates the route the coming soon page which is used when a page isnt created yet.
@app.route("/ComingSoon")
def ComingSoon():
    return render_template("ComingSoon.html")

if __name__ == "__main__":
    app.run(debug=True)
