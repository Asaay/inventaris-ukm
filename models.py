from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    nama          = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin      = db.Column(db.Boolean, default=False)

    peminjaman = db.relationship('Peminjaman', backref='peminjam', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'


class Barang(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    nama       = db.Column(db.String(100), nullable=False)
    kategori   = db.Column(db.String(50), nullable=False)
    kondisi    = db.Column(db.String(50), default='Baik')
    jumlah     = db.Column(db.Integer, default=1)
    keterangan = db.Column(db.Text)

    peminjaman = db.relationship('Peminjaman', backref='barang', lazy=True)

    @property
    def jumlah_dipinjam(self):
        return sum(1 for p in self.peminjaman if p.status == 'dipinjam')

    @property
    def tersedia(self):
        return self.jumlah - self.jumlah_dipinjam

    def __repr__(self):
        return f'<Barang {self.nama}>'


class Peminjaman(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    barang_id       = db.Column(db.Integer, db.ForeignKey('barang.id'), nullable=False)
    tanggal_pinjam  = db.Column(db.DateTime, default=datetime.utcnow)
    tanggal_kembali = db.Column(db.DateTime, nullable=True)
    status          = db.Column(db.String(20), default='dipinjam')

    def __repr__(self):
        return f'<Peminjaman {self.id}>'