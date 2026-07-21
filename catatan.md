# Catatan Proyek Inventaris UKM

## Sesi 1 — Setup
- Lupa `git init`, langsung `git remote add` → error "not a git repository"
- `cd D:\Project` tidak jalan dari drive C: → harus `cd /d`
- Bikin `.gitignore` setelah `git add .` → venv telanjur ter-stage.
  Pelajaran: .gitignore tidak berlaku untuk file yang sudah dilacak,
  harus dibersihkan dulu dengan `git rm -r --cached .`
- Error "dubious ownership" karena drive D:

## Sesi 2 — Database
- `app.run()` memblokir, kode di bawahnya tidak pernah jalan
- `db.create_all()` butuh `with app.app_context():`
- Nama file typo: seedd.py

## Sesi 3 — CRUD
- Hapus harus POST, bukan GET (link bisa terpanggil crawler/prefetch)
- Post/Redirect/Get mencegah data dobel saat user refresh
- Validasi HTML bisa dilewati lewat DevTools → wajib validasi ulang di server
- Barang yang sedang dipinjam tidak boleh dihapus (integritas data)
- `get_or_404()` mencegah crash saat ID tidak ada