from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, BooleanField, SubmitField, SelectField, DecimalField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.file import FileField, FileRequired, FileAllowed

class signup(FlaskForm):
    email = EmailField(validators=[DataRequired()],)
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8)],)
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    address = StringField('Delivery Address', validators=[DataRequired()])
    submit = SubmitField('Submit')

class login(FlaskForm):
    email = EmailField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Submit')

class accountType(FlaskForm):
    accountType = SelectField('Account Type', choices=[("Admin"),("Farmer")], validators=[DataRequired()])
    submit = SubmitField('Submit')

class addNewAdmin(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()], )
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)], )
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class addNewFarmer(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()], )
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)], )
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    description = StringField('Description',validators=[DataRequired()])
    profilepicture = FileField('Profile Picture', validators=[ FileRequired(), FileAllowed(['jpg', 'png'], 'Images only! ') ])
    submit = SubmitField('Submit')

class addNewDriver(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    profilepicture = FileField('Profile Picture', validators=[ FileRequired(), FileAllowed(['jpg', 'png'], 'Images only! ') ])
    submit = SubmitField('Submit')

class addNewProduct(FlaskForm):
    name = StringField("Product Name(include Weight of each packet e.g carrot 500g)", validators=[DataRequired()])
    image = FileField('Product Image', validators=[ FileRequired(), FileAllowed(['jpg', 'png'], 'Images only! ') ])
    price = DecimalField("Price of Product",validators=[DataRequired(), NumberRange(min=0.01, max=10000, message="Price must be between £0.01 and £10,000")])
    amount = IntegerField("Number of Product", validators=[DataRequired()])
    description = StringField("Product Description", validators=[DataRequired()])
    active = BooleanField("Should product be active (check box if yes)")
    expiry = DateField("Expiry Date", validators=[DataRequired()])
    submit = SubmitField("Submit")
