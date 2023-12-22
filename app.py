from flask import Flask, render_template, request, redirect, url_for, flash
import os
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length

app = Flask(__name__)
# Set a secret key for CSRF protection
app.config['SECRET_KEY'] = 'your_secret_key'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash('Login Successful!', 'success')
        return redirect(url_for('home'))

    return render_template('login.html', form=form)

@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        flash('Registration Successful!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', form=form)    

# Sample data (replace with a database in a real application)
tweets = [
    {"author": "User1", "content": "This is a tweet.", "photo": None},
    {"author": "User2", "content": "Another tweet here.", "photo": None},
    # Add more tweets as needed
]


@app.route("/home")
def home():
    return render_template("home2.html", tweets=tweets)


@app.route("/post_tweet", methods=["POST"])
def post_tweet():
    author = request.form.get("author")
    content = request.form.get("content")
    photo = None

    if 'photo' in request.files:
        photo_file = request.files['photo']
        if photo_file.filename != '':
            # Save the photo to the 'uploads' folder
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_file.filename)
            photo_file.save(photo_path)
            photo = photo_file.filename

    if author and content:
        new_tweet = {"author": author, "content": content, "photo": photo}
        tweets.append(new_tweet)

    return redirect(url_for("home"))

if __name__ == "__main__":
    # Ensure the 'uploads' folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(debug=True)

