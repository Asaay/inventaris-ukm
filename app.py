from flask import Flask, render_template
from models import db, User, Barang, Peminjaman

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ganti-ini-nanti-dengan-string-acak'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventaris.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def index():
    daftar_barang = Barang.query.all()
    return render_template('index.html', daftar_barang=daftar_barang)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)