from flask import Flask, render_template, url_for, request, redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import sys

# The following block makes it so that only csv files can be used in the program
ALLOWED_EXTENSIONS = set(['csv'])
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app) # Initialize the database
with app.app_context():
    db.create_all()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods = ['POST', 'GET'])
def index():
    return render_template('upload.html') # Simply render the upload page for now
                                          # May want to replace this with a home page that has the options to check lists or upload files

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    # This page allows the user to upload files to the database (hopefully)
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename): # Make sure the file exists AND is a csv file
            filename = secure_filename(file.filename) # Remove slashes, white space, ec. and replaces with underscores
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], filename)) # Save the file to the 'files' directory
        return redirect(url_for('upload')) # Return the user to the upload page to give the option to upload more files
    
    return render_template('upload.html')

@app.route('/check', methods=["GET", "POST"])
def check():
    # This page will allow you to select a BOX list and a MASTER list, out of the files you have uploaded, to compare against eachother
    return render_template('check.html')

if __name__ == '__main__':
    app.run(debug = True)
