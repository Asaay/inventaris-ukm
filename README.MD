# Sistem Inventaris UKM Telkom Art

Aplikasi web untuk mencatat inventaris dan peminjaman barang UKM.
Dibangun untuk menyelesaikan masalah nyata: pencatatan peminjaman
alat musik dan properti yang sebelumnya dilakukan manual, sehingga
sering tidak jelas siapa yang sedang meminjam apa.

## Status

🚧 Dalam pengembangan — fitur CRUD selesai, autentikasi sedang dikerjakan.

## Fitur

- [x] Daftar inventaris dengan status ketersediaan real-time
- [x] Tambah, ubah, dan hapus data barang
- [x] Validasi input di sisi server
- [x] Notifikasi hasil aksi (flash message)
- [ ] Autentikasi pengguna
- [ ] Pencatatan peminjaman dan pengembalian
- [ ] Dashboard admin

## Tech Stack

| Lapisan | Teknologi |
|---|---|
| Backend | Python, Flask |
| ORM | SQLAlchemy |
| Database | SQLite |
| Frontend | Jinja2, Bootstrap 5 |

## Rancangan Database

Tiga entitas utama dengan relasi many-to-many yang membawa data tambahan:

- **User** — data anggota
- **Barang** — data inventaris
- **Peminjaman** — tabel penghubung, menyimpan tanggal pinjam,
  tanggal kembali, dan status

Jumlah barang yang tersedia tidak disimpan sebagai kolom, melainkan
dihitung saat dibutuhkan dari data peminjaman aktif. Ini mencegah
data menjadi tidak sinkron.

## Menjalankan Secara Lokal

```bash
git clone https://github.com/Asaay/inventaris-ukm.git
cd inventaris-ukm

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt

python seed.py               # isi data awal
python app.py
```

Buka `http://127.0.0.1:5000`

## Catatan Pengembangan

Beberapa keputusan teknis yang diambil:

- **Penghapusan menggunakan method POST, bukan GET.** Link GET bisa
  terpanggil oleh crawler atau prefetch browser tanpa ada yang mengklik.
- **Pola Post/Redirect/Get** diterapkan setelah penyimpanan, agar data
  tidak tersimpan ganda ketika pengguna me-refresh halaman.
- **Validasi dilakukan ulang di sisi server**, karena atribut `required`
  pada HTML dapat dilewati melalui DevTools.
- **Barang yang sedang dipinjam tidak dapat dihapus**, untuk menjaga
  integritas relasi dengan tabel Peminjaman.

## Pengembang

Asril Gufta Bimatara — [GitHub](https://github.com/Asaay)