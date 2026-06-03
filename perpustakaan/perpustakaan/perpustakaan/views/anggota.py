from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import FieldError
from datetime import timedelta
from ..models import Anggota
from .base import BaseView

class AnggotaView(BaseView):
    def __tambah_anggota(self, data):
        anggota = Anggota()
        anggota.nama       = data.get('nama', '')
        anggota.id_anggota = data.get('id_anggota', '')
        anggota.email      = data.get('email', '')
        anggota.save()

    def __edit_anggota(self, data):
        pk = data.get('pk')
        anggota = get_object_or_404(Anggota, pk=pk)
        anggota.nama       = data.get('nama', anggota.nama)
        anggota.id_anggota = data.get('id_anggota', anggota.id_anggota)
        anggota.email      = data.get('email', anggota.email)
        anggota.save()

    def __hapus_anggota(self, pk):
        Anggota.objects.filter(pk=pk).delete()

    def handle(self, request, pk=None):
        cek = self._redirect_if_not_login(request)
        if cek:
            return cek

        if request.method == 'POST':
            aksi = request.POST.get('aksi')
            try:
                if aksi == 'tambah':
                    self.__tambah_anggota(request.POST)
                    messages.success(request, 'Anggota berhasil didaftarkan!')
                elif aksi == 'edit': 
                    self.__edit_anggota(request.POST)
                    messages.success(request, 'Data anggota berhasil diperbarui!')
                elif aksi == 'hapus' and pk:
                    self.__hapus_anggota(pk)
                    messages.success(request, 'Anggota berhasil dihapus dari sistem!')
            except ValueError as e:
                messages.error(request, str(e))
            
            return redirect('kelola_anggota')

        anggota_list = Anggota.objects.all()
        batas_waktu = timezone.now() - timedelta(days=7)
        try:
            anggota_baru_count = Anggota.objects.filter(created_at__gte=batas_waktu).count()
        except FieldError:
            anggota_baru_count = 0

        return render(request, 'frontend/daftar_anggota.html', {
            'anggota_list': anggota_list,
            'anggota_baru_count': anggota_baru_count
        })