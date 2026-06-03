# 📚✨ Sistem Manajemen Perpustakaan Wiyung ✨📚

## Deskripsi Project
**Perpustakaan Wiyung** adalah sistem aplikasi manajemen perpustakaan terpadu yang dibangun menggunakan **Python** dan *framework* **Django**. Sistem ini hadir sebagai asisten virtual yang mempermudah tugas administrator perpustakaan dalam melacak sirkulasi buku, memantau ketersediaan stok, mengelola data anggota, hingga menghitung denda keterlambatan secara otomatis. 

Antarmuka proyek ini menggunakan gaya Neo-Brutalism dengan vanilla HTML, CSS, dan JavaScript. Selain fungsional, proyek ini dirancang dengan arsitektur *backend* yang terstruktur menerapkan 4 pilar utama **Object-Oriented Programming (OOP)** secara kokoh dan pola *Singleton-like* pada konfigurasi penanganan *routing* HTTP.

---

## Anggota Kelompok
Proyek ini dikembangkan penuh cinta dan kolaborasi oleh tim kami:

| Nama Anggota | NIM |
| :--- | :---: |
| 🦦 **Alvito Wahyu Dwi Nofa** | `25051204031` |
| 🦝 **Muhammad Fawwaz Taufiqul Hakim** | `25051204175` |
| 🐈 **Calvin Azarya Pravita Yuwono** | `25051204177` |
| 🐰 **Aliya Shafia** | `25051204200` |

---

## Fitur Utama

* **Smart Dashboard & Statistik Real-Time**
  Pusat informasi (kendali utama) yang memberikan ringkasan data secara *live*. Di dalam *dashboard* ini admin dapat melihat:
  * **Kartu Metrik Utama:** Menampilkan angka pasti dari Total Koleksi Buku, jumlah Anggota Aktif, jumlah Buku yang Sedang Dipinjam, dan blok peringatan khusus berwarna merah untuk Pinjaman Terlambat.
  * **Tren Peminjaman Realtime:** Visualisasi grafik batang (*bar chart*) interaktif yang menunjukkan aktivitas peminjaman per hari.
  * **Aktivitas Terbaru:** Tabel ringkasan sirkulasi (peminjaman dan pengembalian) yang paling baru dilakukan, lengkap dengan status dan tenggat waktunya.
  * **Indikator Waktu:** Penunjuk jam dan tanggal sistem yang berjalan secara interaktif dan langsung (*live*).

* **Manajemen Koleksi Buku (CRUD)**
  Pencatatan buku komprehensif dengan perlindungan validasi ketersediaan dan manipulasi status stok (*stok terenkapsulasi agar tidak pernah bernilai negatif*).

* **Manajemen Data Anggota (CRUD)**
  Pencatatan profil anggota dengan proteksi validasi ekstrak (contoh: memverifikasi jika email wajib mengandung karakter `@`).
  
* **Sistem Transaksi Peminjaman (Sirkulasi)**
  Fitur pencatatan pintar untuk alur peminjaman. Sistem secara otomatis mendeteksi pembaruan *status* (Dipinjam / Terlambat / Kembali) dan melakukan perhitungan denda keterlambatan secara otomatis (melalui relasi *Foreign Key* ke tabel Buku & Anggota).

* **Konfigurasi Sistem Dinamis (Settings)**
  Memungkinkan admin untuk menyesuaikan variabel aturan perpustakaan secara langsung melalui antarmuka, seperti menetapkan tarif denda per hari, batas maksimal peminjaman buku, dan lama hari durasi pinjam tanpa perlu memodifikasi *source code*.

---

## Cara Menjalankan Project
Ikuti panduan komprehensif berikut untuk melakukan instalasi dan inisialisasi awal proyek di lingkungan komputermu:

1. **Pengunduhan Repositori Kode Sumber (Clone Repository)**
   Mengunduh repositori proyek secara utuh dari GitHub dan masuk ke direktori lokal.
   ```bash
   git clone https://github.com/calvinyuwono88-ship-it/perpustakaan.git
   cd perpustakaan
   ```

2. **Buat & Aktifkan Virtual Environment**
   ```bash
   python -m venv env
   # Untuk OS Windows:
   env\Scripts\activate
   # Untuk OS Linux/macOS:
   source env/bin/activate
   ```

3. **4. Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan Migrasi Database**
   Sistem menggunakan SQLite3 terintegrasi, lakukan migrasi:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Buat Akun Admin (Superuser)**
   Digunakan untuk mengakses fungsionalitas dasbor administrasi aplikasi secara penuh.
   ```bash
   python manage.py createsuperuser
   ```
   
6. **Jalankan Server Lokal**
   ```bash
   python manage.py runserver
   ```
   Lalu Buka `http://127.0.0.1:8000/` di *browser* Anda dan _login_ dengan akun (Username dan Password) superuser yang telah dibuat.
   
---

## Penjelasan Implementasi OOP
Sistem ini dirancang sangat berstruktur dengan mematuhi 4 pilar OOP Python secara ketat yang dikorelasikan pada arsitektur Model dan View:

1.  **Abstraksi (*Abstraction*):**
   * Model: Sistem menggunakan BaseModel (abstract = True) sebagai cetak biru (kerangka dasar) wajib untuk seluruh tabel entitas. Kelas ini menyediakan fondasi berupa fungsi get_info() yang wajib di-override oleh subkelasnya. Jika tidak diimplementasikan, sistem akan otomatis melempar eksepsi NotImplementedError.
   * Views: Terdapat BaseView yang bertindak sebagai antarmuka abstrak murni, di mana setiap subkelas controller halaman diwajibkan untuk mengimplementasikan fungsi penanganan spesifik, yaitu .handle().

2.  **Pewarisan (*Inheritance*):**  
   * Model: Entitas utama dalam sistem seperti Buku, Anggota, Pinjaman, dan Konfigurasi merupakan kelas turunan dari BaseModel. Mekanisme ini membuat seluruh entitas tersebut secara otomatis memiliki fungsionalitas dan atribut standar, seperti kolom pemantauan waktu (created_at dan updated_at).
   * Views: Seluruh class controller halaman juga mewarisi BaseView. Hal ini memungkinkan semua halaman untuk menggunakan fungsionalitas keamanan terpusat secara langsung, seperti mekanisme pengecekan hak akses sesi menggunakan metode _redirect_if_not_login().

3.  **Enkapsulasi (*Encapsulation*):**  
   * Proteksi Atribut: Variabel data yang rentan dilindungi menggunakan konvensi hak akses private/protected, seperti atribut _stok pada entitas Buku dan _email pada entitas Anggota.

   * Validasi Setter/Getter: Modul eksternal tidak dapat mengubah data ini secara sepihak. Akses dan modifikasi hanya bisa dilakukan melalui Decorator Property (Getter & Setter) untuk memvalidasi nilai (contoh: sistem akan menolak atau melempar error jika stok buku diatur menjadi <= 0).

   * Proteksi Logika Bisnis: Proses kalkulasi yang kompleks disembunyikan dengan rapi agar tidak terekspos ke modul luar. Contohnya adalah penggunaan private method __hitung_keterlambatan() pada entitas Pinjaman untuk menghitung lama waktu denda secara aman.

4.  **Polimorfisme (*Polymorphism*):**  
   * Method Overriding: Setiap subkelas model memiliki implementasi berbeda (spesifik) saat menjalankan fungsi get_info() turunan dari BaseModel.
   * Dynamic Output (__str__): Pemanggilan fungsi representasi string bawaan sistem (__str__()) akan memberikan output yang dinamis menyesuaikan objek pemanggilnya tanpa harus mengubah alur pemanggilan:

      1. Objek Buku akan mengembalikan label informasi stok.

      2. Objek Anggota akan mengembalikan identitas ID anggota.

      3. Objek Pinjaman akan mengembalikan status kalkulasi waktu pinjam beserta nominal rupiah dari denda keterlambatan secara otomatis.
    
## 📸 Screenshots Program

1. **Menu Login**
   <img width="1918" height="915" alt="Cuplikan layar 2026-06-03 185442" src="https://github.com/user-attachments/assets/c5abd774-cb02-46cb-87c2-2605af4994f7" />
2. **Halaman Utama**
   <img width="1897" height="917" alt="Cuplikan layar 2026-06-03 185644" src="https://github.com/user-attachments/assets/65f03de1-4fc2-4a79-956e-4397bd984540" />
3. **Daftar Buku**
   <img width="1896" height="918" alt="Cuplikan layar 2026-06-03 185819" src="https://github.com/user-attachments/assets/20659b54-2f3b-4e8a-8f31-64d13661507f" />
   <img width="1900" height="918" alt="Cuplikan layar 2026-06-03 185850" src="https://github.com/user-attachments/assets/4adba4c9-16be-4570-9fce-859e46f8a1ec" />
   <img width="1896" height="915" alt="Cuplikan layar 2026-06-03 185913" src="https://github.com/user-attachments/assets/825127ae-fc2b-419e-b989-98f4e4baffe7" />
4. **Daftar Anggota**
   <img width="1899" height="917" alt="Cuplikan layar 2026-06-03 190749" src="https://github.com/user-attachments/assets/acd0b80e-f83b-4b51-aaeb-b094c246f6d1" />
   <img width="1898" height="916" alt="Cuplikan layar 2026-06-03 190804" src="https://github.com/user-attachments/assets/f1ceac36-9c0d-48f7-aba2-ee7703887bb1" />
   <img width="1900" height="912" alt="Cuplikan layar 2026-06-03 190824" src="https://github.com/user-attachments/assets/154c27ec-b5fe-4e78-af28-37b1d4cd10ec" />
5. **Catatan Peminjaman**
   <img width="1898" height="918" alt="Cuplikan layar 2026-06-03 191439" src="https://github.com/user-attachments/assets/53c5e8c9-ba70-4153-abc4-9bb6d0b5309b" />
   <img width="1899" height="919" alt="Cuplikan layar 2026-06-03 191454" src="https://github.com/user-attachments/assets/e4f47960-fe66-42b1-9861-bf09e0d0ea44" />
6. **Settings
   <img width="1899" height="916" alt="Cuplikan layar 2026-06-03 191842" src="https://github.com/user-attachments/assets/38b4bdc2-1315-4c0b-b051-a44826dbc01c" />
   <img width="1899" height="918" alt="Cuplikan layar 2026-06-03 191904" src="https://github.com/user-attachments/assets/7bc6e5af-b8f0-4f87-b9ed-0107ef02cbfb" />
   <img width="1898" height="914" alt="Cuplikan layar 2026-06-03 191942" src="https://github.com/user-attachments/assets/8a37ecb8-df23-43ce-b465-f8b19b6919da" />










