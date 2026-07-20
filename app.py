from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User, Barang, Peminjaman

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ganti-ini-nanti-dengan-string-acak'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventaris.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

KATEGORI = ['Alat Musik', 'Kostum', 'Audio', 'Properti', 'Lainnya']
KONDISI  = ['Baik', 'Rusak Ringan', 'Rusak Berat']


# ---------- READ ----------
@app.route('/')
def index():
    daftar_barang = Barang.query.order_by(Barang.nama).all()
    return render_template('index.html', daftar_barang=daftar_barang)


# ---------- CREATE ----------
@app.route('/barang/tambah', methods=['GET', 'POST'])
def tambah_barang():
    if request.method == 'POST':
        nama       = request.form.get('nama', '').strip()
        kategori   = request.form.get('kategori', '')
        kondisi    = request.form.get('kondisi', 'Baik')
        jumlah     = request.form.get('jumlah', '')
        keterangan = request.form.get('keterangan', '').strip()

        error = validasi(nama, kategori, kondisi, jumlah)
        if error:
            flash(error, 'danger')
            return render_template('form_barang.html', mode='tambah',
                                   kategori_list=KATEGORI, kondisi_list=KONDISI,
                                   data=request.form)

        barang = Barang(nama=nama, kategori=kategori, kondisi=kondisi,
                        jumlah=int(jumlah), keterangan=keterangan)
        db.session.add(barang)
        db.session.commit()

        flash(f'Barang "{nama}" berhasil ditambahkan.', 'success')
        return redirect(url_for('index'))

    return render_template('form_barang.html', mode='tambah',
                           kategori_list=KATEGORI, kondisi_list=KONDISI, data={})


# ---------- UPDATE ----------
@app.route('/barang/<int:id>/edit', methods=['GET', 'POST'])
def edit_barang(id):
    barang = Barang.query.get_or_404(id)

    if request.method == 'POST':
        nama       = request.form.get('nama', '').strip()
        kategori   = request.form.get('kategori', '')
        kondisi    = request.form.get('kondisi', 'Baik')
        jumlah     = request.form.get('jumlah', '')
        keterangan = request.form.get('keterangan', '').strip()

        error = validasi(nama, kategori, kondisi, jumlah)
        if not error and int(jumlah) < barang.jumlah_dipinjam:
            error = (f'Jumlah tidak boleh kurang dari yang sedang dipinjam '
                     f'({barang.jumlah_dipinjam}).')

        if error:
            flash(error, 'danger')
            return render_template('form_barang.html', mode='edit',
                                   kategori_list=KATEGORI, kondisi_list=KONDISI,
                                   data=request.form, barang=barang)

        barang.nama       = nama
        barang.kategori   = kategori
        barang.kondisi    = kondisi
        barang.jumlah     = int(jumlah)
        barang.keterangan = keterangan
        db.session.commit()

        flash(f'Barang "{nama}" berhasil diperbarui.', 'success')
        return redirect(url_for('index'))

    return render_template('form_barang.html', mode='edit',
                           kategori_list=KATEGORI, kondisi_list=KONDISI,
                           data=barang.__dict__, barang=barang)


# ---------- DELETE ----------
@app.route('/barang/<int:id>/hapus', methods=['POST'])
def hapus_barang(id):
    barang = Barang.query.get_or_404(id)

    if barang.jumlah_dipinjam > 0:
        flash(f'"{barang.nama}" tidak bisa dihapus karena sedang dipinjam.', 'danger')
        return redirect(url_for('index'))

    nama = barang.nama
    db.session.delete(barang)
    db.session.commit()

    flash(f'Barang "{nama}" berhasil dihapus.', 'success')
    return redirect(url_for('index'))


# ---------- Helper ----------
def validasi(nama, kategori, kondisi, jumlah):
    if not nama:
        return 'Nama barang wajib diisi.'
    if len(nama) > 100:
        return 'Nama barang maksimal 100 karakter.'
    if kategori not in KATEGORI:
        return 'Kategori tidak valid.'
    if kondisi not in KONDISI:
        return 'Kondisi tidak valid.'
    if not jumlah.isdigit():
        return 'Jumlah harus berupa angka.'
    if int(jumlah) < 1:
        return 'Jumlah minimal 1.'
    return None


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)