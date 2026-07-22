from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)
from models import db, User, Barang, Peminjaman
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'kunci-dev-lokal')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventaris.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Silakan login terlebih dahulu.'
login_manager.login_message_category = 'warning'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

# ---------- REGISTER ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        nama     = request.form.get('nama', '').strip()
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        password2 = request.form.get('password2', '')

        if not nama or not email or not password:
            flash('Semua kolom wajib diisi.', 'danger')
        elif password != password2:
            flash('Konfirmasi password tidak cocok.', 'danger')
        elif len(password) < 6:
            flash('Password minimal 6 karakter.', 'danger')
        elif User.query.filter_by(email=email).first():
            flash('Email sudah terdaftar.', 'danger')
        else:
            user = User(nama=nama, email=email)
            user.set_password(password)
            # pengguna pertama otomatis jadi admin
            if User.query.count() == 0:
                user.is_admin = True
            db.session.add(user)
            db.session.commit()
            flash('Registrasi berhasil. Silakan login.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')


# ---------- LOGIN ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f'Selamat datang, {user.nama}.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Email atau password salah.', 'danger')

    return render_template('login.html')


# ---------- LOGOUT ----------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('login'))


KATEGORI = ['Alat Musik', 'Kostum', 'Audio', 'Properti', 'Lainnya']
KONDISI  = ['Baik', 'Rusak Ringan', 'Rusak Berat']


# ---------- READ ----------
@app.route('/')
def index():
    daftar_barang = Barang.query.order_by(Barang.nama).all()
    return render_template('index.html', daftar_barang=daftar_barang)


# ---------- CREATE ----------
@app.route('/barang/tambah', methods=['GET', 'POST'])
@login_required
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
@login_required
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
@login_required
def hapus_barang(id):
    if not current_user.is_admin:
        flash('Hanya admin yang dapat menghapus barang.', 'danger')
        return redirect(url_for('index'))

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


# ---------- PINJAM ----------
@app.route('/barang/<int:id>/pinjam', methods=['POST'])
@login_required
def pinjam_barang(id):
    barang = Barang.query.get_or_404(id)

    if barang.tersedia < 1:
        flash(f'"{barang.nama}" sedang tidak tersedia.', 'danger')
        return redirect(url_for('index'))

    # cegah pinjam barang yang sama dua kali sekaligus
    sudah_pinjam = Peminjaman.query.filter_by(
        user_id=current_user.id, barang_id=id, status='dipinjam').first()
    if sudah_pinjam:
        flash(f'Anda sudah meminjam "{barang.nama}".', 'warning')
        return redirect(url_for('index'))

    peminjaman = Peminjaman(user_id=current_user.id, barang_id=id)
    db.session.add(peminjaman)
    db.session.commit()

    flash(f'Anda meminjam "{barang.nama}".', 'success')
    return redirect(url_for('index'))


# ---------- KEMBALIKAN ----------
@app.route('/peminjaman/<int:id>/kembalikan', methods=['POST'])
@login_required
def kembalikan_barang(id):
    peminjaman = Peminjaman.query.get_or_404(id)

    # hanya peminjam sendiri atau admin yang boleh mengembalikan
    if peminjaman.user_id != current_user.id and not current_user.is_admin:
        flash('Anda tidak berhak mengembalikan peminjaman ini.', 'danger')
        return redirect(url_for('index'))

    peminjaman.status = 'selesai'
    peminjaman.tanggal_kembali = datetime.utcnow()
    db.session.commit()

    flash(f'"{peminjaman.barang.nama}" berhasil dikembalikan.', 'success')
    return redirect(url_for('peminjaman_saya'))


# ---------- DAFTAR PEMINJAMAN SAYA ----------
@app.route('/peminjaman')
@login_required
def peminjaman_saya():
    daftar = Peminjaman.query.filter_by(
        user_id=current_user.id).order_by(Peminjaman.tanggal_pinjam.desc()).all()
    return render_template('peminjaman.html', daftar=daftar)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)