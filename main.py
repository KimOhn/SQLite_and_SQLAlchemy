from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"

db.create_all()


@app.route('/',methods = ["GET", "POST"])
def home():
    all_books = db.session.query(Book).all()
    return render_template("index.html", rated_books = all_books)


@app.route("/add", methods = ["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(
            title = request.form["book_name"],
            author = request.form["author"],
            rating = request.form["rating"]
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")

@app.route("/edit/", methods = ["GET", "POST"])
def edit():
    if request.method == "POST":
        key = request.form["id"]
        rating_to_update = Book.query.get(key)
        rating_to_update.rating = request.form["new_rating"]
        db.session.commit()
        return redirect(url_for('home'))
    primary_key = request.args.get('id')
    book_to_update = Book.query.get(primary_key)
    return render_template("edit.html", to_update = book_to_update)

@app.route("/delete/")
def delete():
    primary_key = request.args.get('id')
    book_to_delete = Book.query.get(primary_key)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))
if __name__ == "__main__":
    app.run(debug=True)

