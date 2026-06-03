from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Buku, Pinjaman
from .base import BaseView

class BukuView(BaseView):
    def __tambah_buku(self, data):
        buku = Buku()
        buku.judul    = data.get('judul', '')
        buku.penulis  = data.get('penulis', '')
        buku.kategori = data.get('kategori', '')
        buku.stok     = int(data.get('stok', 0))
        buku.save()
    

    def __hapus_buku(self, pk):
        Buku.objects.filter(pk=pk).delete()

    def handle(self, request, pk=None):
        cek = self._redirect_if_not_login(request)
        if cek:
            return cek

        if request.method == 'POST':
            aksi = request.POST.get('aksi')
            if aksi == 'tambah':
                try:
                    self.__tambah_buku(request.POST)
                    messages.success(request, 'Buku berhasil ditambahkan!')
                except ValueError as e:
                    messages.error(request, str(e))
            elif aksi == 'hapus' and pk:
                self.__hapus_buku(pk)
                messages.success(request, 'Buku berhasil dihapus!')
            return redirect('kelola_buku')

        buku_list = Buku.objects.all()
        
        total_dipinjam = Pinjaman.objects.filter(status__iexact='dipinjam').count()

        context = {
            'buku_list': buku_list,
            'total_dipinjam': total_dipinjam,
        }

        return render(request, 'frontend/manajemen_buku.html', context)
    
    def __edit_buku(self, pk, data):
        buku = Buku.objects.get(pk=pk)
        buku.judul    = data.get('judul', buku.judul)
        buku.penulis  = data.get('penulis', buku.penulis)
        buku.kategori = data.get('kategori', buku.kategori)
        buku.stok     = int(data.get('stok', buku.stok))
        buku.save()

    def handle_edit(self, request, pk):
        cek = self._redirect_if_not_login(request)
        if cek:
            return cek

        buku = Buku.objects.get(pk=pk)

        if request.method == 'POST':
            try:
                self.__edit_buku(pk, request.POST)
                messages.success(request, f'Buku "{buku.judul}" berhasil diperbarui!')
                return redirect('kelola_buku')
            except ValueError as e:
                messages.error(request, str(e))
        
        return render(request, 'frontend/edit_buku.html', {'buku': buku})