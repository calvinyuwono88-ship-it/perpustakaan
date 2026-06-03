from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import FieldError
from datetime import date, timedelta
from ..models import Buku, Anggota, Pinjaman, Konfigurasi
from .base import BaseView

class PinjamanView(BaseView):
    def __buat_pinjaman(self, data):
        buku    = get_object_or_404(Buku, pk=data.get('buku_id'))
        anggota = get_object_or_404(Anggota, pk=data.get('anggota_id'))
        konfig  = Konfigurasi.objects.first()
        durasi  = konfig.durasi_pinjam if konfig else 7

        if not buku.tersedia():
            raise ValueError(f"Stok buku '{buku.judul}' habis!")

        Pinjaman.objects.create(
            buku=buku,
            anggota=anggota,
            jatuh_tempo=date.today() + timedelta(days=durasi)
        )
        buku.stok -= 1  
        buku.save()

    def __proses_kembali(self, pk):
        pinjaman = get_object_or_404(Pinjaman, pk=pk)
        pinjaman.status = 'kembali'
        pinjaman.save()
        pinjaman.buku.stok += 1
        pinjaman.buku.save()

    def __hapus_pinjaman(self, pk):
        Pinjaman.objects.filter(pk=pk).delete()

    def handle(self, request, pk=None):
        cek = self._redirect_if_not_login(request)
        if cek:
            return cek

        if request.method == 'POST':
            aksi = request.POST.get('aksi')
            try:
                if aksi == 'pinjam':
                    self.__buat_pinjaman(request.POST)
                    messages.success(request, 'Pinjaman berhasil dicatat!')
                elif aksi == 'kembali' and pk:
                    self.__proses_kembali(pk)
                    messages.success(request, 'Buku berhasil dikembalikan!')
                elif aksi == 'hapus' and pk:
                    self.__hapus_pinjaman(pk)
                    messages.success(request, 'Catatan transaksi berhasil dihapus!')
            except ValueError as e:
                messages.error(request, str(e))
            return redirect('catatan_pinjaman')

        pinjaman_list = Pinjaman.objects.select_related('buku', 'anggota').all().order_by('-created_at')
        buku_list     = Buku.objects.filter(_stok__gt=0) 
        anggota_list  = Anggota.objects.all()

        aktif_dipinjam_count = Pinjaman.objects.filter(status='dipinjam').count()
        terlambat_count      = Pinjaman.objects.filter(status='terlambat').count()
        diperpanjang_count   = Pinjaman.objects.filter(status='diperpanjang').count()
        
        try:
            kembali_hari_ini_count = Pinjaman.objects.filter(status='kembali', tanggal_kembali=date.today()).count()
        except FieldError:
            kembali_hari_ini_count = Pinjaman.objects.filter(status='kembali').count()

        return render(request, 'frontend/catatan_pinjaman.html', {
            'pinjaman_list': pinjaman_list,
            'buku_list'    : buku_list,
            'anggota_list' : anggota_list,
            'aktif_dipinjam_count': aktif_dipinjam_count,
            'terlambat_count': terlambat_count,
            'diperpanjang_count': diperpanjang_count,
            'kembali_hari_ini_count': kembali_hari_ini_count,
        })