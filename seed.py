from app import app
from models import db, Barang

data_awal = [
    {"nama": "Gitar Akustik Yamaha", "kategori": "Alat Musik", "jumlah": 2},
    {"nama": "Keyboard Casio",       "kategori": "Alat Musik", "jumlah": 1},
    {"nama": "Kostum Tari Saman",    "kategori": "Kostum",     "jumlah": 10},
    {"nama": "Standing Mic",         "kategori": "Audio",      "jumlah": 4},
    {"nama": "Lampu Sorot",          "kategori": "Properti",   "jumlah": 6},
]

with app.app_context():
    db.create_all()
    for d in data_awal:
        db.session.add(Barang(**d))
    db.session.commit()
    print(f"{len(data_awal)} barang berhasil ditambahkan.")