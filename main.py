from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Flask

app = Flask(__name__)

# Create the new DB

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)


# Create the Book Table
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=False, nullable=False)
    rating = db.Column(db.Float, nullable=False)


# Read all the books
def get_single_book(title):
    return db.session.execute(db.select(Book).filter_by(title=title)).scalar_one()


@app.route('/')
def home():
    db.create_all()
    all_books = db.session.query(Book).all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        db.session.add(new_book)
        db.session.commit()
    return render_template("add.html")


@app.route("/edit/<title>", methods=["GET", "POST"])
def edit_book(title):
    book = get_single_book(title)
    if request.method == "POST":
        book.rating = request.form["new_rating"]
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", title=book.title, rating=book.rating)

@app.route("/delete/<title>")
def delete(title):
    book = get_single_book(title)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

