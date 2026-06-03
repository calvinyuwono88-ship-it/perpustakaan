from django.db import models
from abc import abstractmethod
from datetime import date, timedelta


# ABSTRACTION Abstract base class
class BaseModel(models.Model):
    """
    Kelas abstrak sebagai fondasi semua model.
    Menyimpan field umum: created_at dan updated_at.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  

    def get_info(self):
        """Method yang WAJIB di-override oleh semua turunan (Abstraksi)"""
        raise NotImplementedError("Subclass harus mengimplementasikan get_info()")

    def __str__(self):
        return self.get_info()



# INHERITANCE Buku mewarisi BaseModel
class Buku(BaseModel):
    """
    Model Buku — mewarisi BaseModel (Inheritance).
    Menerapkan enkapsulasi pada field stok via property.
    """
    judul    = models.CharField(max_length=200)
    penulis  = models.CharField(max_length=100)
    kategori = models.CharField(max_length=50, blank=True)
    _stok    = models.IntegerField(default=0, db_column='stok')  # ENCAPSULATION


    # ENCAPSULATION Akses stok hanya lewat property,
    @property
    def stok(self):
        """Getter stok — baca nilai stok"""
        return self._stok

    @stok.setter
    def stok(self, nilai):
        """Setter stok — validasi sebelum simpan"""
        if nilai < 0:
            raise ValueError("Stok tidak boleh negatif!")
        self._stok = nilai

    def tersedia(self):
        """Cek apakah buku masih tersedia untuk dipinjam"""
        return self._stok > 0

    # POLYMORPHISM Override get_info() dari BaseModel
    def get_info(self):
        return f"[BUKU] {self.judul} oleh {self.penulis} (Stok: {self._stok})"



# INHERITANCE Anggota mewarisi BaseModel

class Anggota(BaseModel):
    """
    Model Anggota — mewarisi BaseModel (Inheritance).
    Enkapsulasi pada field email dengan validasi.
    """
    nama       = models.CharField(max_length=100)
    id_anggota = models.CharField(max_length=20, unique=True)
    _email     = models.EmailField(db_column='email')  # ENCAPSULATION

    @property
    def email(self):
        """Getter email"""
        return self._email

    @email.setter
    def email(self, nilai):
        """Setter email — pastikan ada karakter @"""
        if '@' not in str(nilai):
            raise ValueError("Format email tidak valid!")
        self._email = nilai

    def total_pinjaman_aktif(self):
        """Hitung berapa buku yang sedang dipinjam anggota ini"""
        return self.pinjaman_set.filter(status='dipinjam').count()

    # POLYMORPHISM Override get_info() dari BaseModel
    def get_info(self):
        return f"[ANGGOTA] {self.nama} | ID: {self.id_anggota} | Email: {self._email}"


# INHERITANCE Pinjaman mewarisi BaseModel
class Pinjaman(BaseModel):
    """
    Model Pinjaman — relasi antara Buku dan Anggota.
    Mewarisi BaseModel dan meng-override get_info() secara berbeda
    dibanding Buku dan Anggota (Polymorphism).
    """
    STATUS_CHOICES = [
        ('dipinjam',  'Dipinjam'),
        ('terlambat', 'Terlambat'),
        ('kembali',   'Dikembalikan'),
    ]

    buku         = models.ForeignKey(Buku, on_delete=models.CASCADE)
    anggota      = models.ForeignKey(Anggota, on_delete=models.CASCADE)
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='dipinjam')
    tanggal_pinjam = models.DateField(auto_now_add=True)
    jatuh_tempo  = models.DateField()


    # ENCAPSULATION Logika hitung denda disembunyikan di dalam
    def __hitung_keterlambatan(self):
        """Private method — hitung hari keterlambatan"""
        if date.today() > self.jatuh_tempo:
            return (date.today() - self.jatuh_tempo).days
        return 0

    def hitung_denda(self):
        """
        Public method — pakai hasil private method di atas.
        Enkapsulasi: detail perhitungan tersembunyi dari luar.
        """
        konfig    = Konfigurasi.objects.first()
        tarif     = konfig.denda_per_hari if konfig else 2000
        maks      = konfig.maks_denda if konfig else 50000
        hari_telat = self.__hitung_keterlambatan()
        denda     = hari_telat * tarif
        return min(denda, maks)

    def perbarui_status(self):
        """Update status otomatis berdasarkan tanggal hari ini"""
        if self.status != 'kembali':
            if date.today() > self.jatuh_tempo:
                self.status = 'terlambat'
            else:
                self.status = 'dipinjam'
            self.save()

    # POLYMORPHISM
    def get_info(self):
        return f"[PINJAMAN] {self.anggota.nama} meminjam '{self.buku.judul}' | Status: {self.status} | Denda: Rp{self.hitung_denda():,}"



# INHERITANCE Konfigurasi mewarisi BaseModel
class Konfigurasi(BaseModel):
    """
    Model Konfigurasi — pengaturan sistem perpustakaan.
    Hanya boleh ada 1 baris data (singleton pattern).
    """
    denda_per_hari = models.IntegerField(default=2000)
    maks_denda     = models.IntegerField(default=50000)
    durasi_pinjam  = models.IntegerField(default=7)
    maks_buku      = models.IntegerField(default=3)

    # POLYMORPHISM
    def get_info(self):
        return f"[KONFIGURASI] Denda: Rp{self.denda_per_hari}/hari | Durasi: {self.durasi_pinjam} hari | Maks buku: {self.maks_buku}"