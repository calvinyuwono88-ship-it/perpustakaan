from django.contrib import admin
from .models import Buku, Anggota, Pinjaman, Konfigurasi

# Daftarkan semua model agar bisa diakses di admin
@admin.register(Buku)
class BukuAdmin(admin.ModelAdmin):
    list_display  = ('judul', 'penulis', 'kategori', '_stok')
    search_fields = ('judul', 'penulis')

@admin.register(Anggota)
class AnggotaAdmin(admin.ModelAdmin):
    list_display  = ('nama', 'id_anggota', '_email')
    search_fields = ('nama', 'id_anggota')

@admin.register(Pinjaman)
class PinjamanAdmin(admin.ModelAdmin):
    list_display  = ('buku', 'anggota', 'status', 'jatuh_tempo')
    list_filter   = ('status',)

@admin.register(Konfigurasi)
class KonfigurasiAdmin(admin.ModelAdmin):
    list_display = ('denda_per_hari', 'maks_denda', 'durasi_pinjam', 'maks_buku')