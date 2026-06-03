from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from ..models import Konfigurasi
from .base import BaseView

class SettingsView(BaseView):
    def __update_profile(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        if User.objects.filter(username=username).exclude(id=request.user.id).exists():
            raise ValueError("Username sudah digunakan oleh admin lain!")
            
        request.user.username = username
        request.user.email = email
        request.user.save()

    def __change_password(self, request):
        current_pass = request.POST.get('current_password')
        new_pass = request.POST.get('new_password')
        confirm_pass = request.POST.get('confirm_password')

        if not request.user.check_password(current_pass):
            raise ValueError("Kata sandi saat ini yang Anda masukkan salah!")
        if new_pass != confirm_pass:
            raise ValueError("Konfirmasi kata sandi baru tidak cocok!")
        if len(new_pass) < 4:
            raise ValueError("Kata sandi baru terlalu pendek (minimal 4 karakter)!")
            
        request.user.set_password(new_pass)
        request.user.save()
        update_session_auth_hash(request, request.user)

    def __update_circulation(self, konfig, data):
        if hasattr(konfig, 'nama_perpustakaan'):
            konfig.nama_perpustakaan = data.get('nama_perpustakaan', 'Perpustakaan Wiyung')
            
        konfig.denda_per_hari = int(data.get('denda_per_hari', 1000))
        konfig.durasi_pinjam  = int(data.get('durasi_pinjam', 14))
        konfig.maks_denda     = int(data.get('maks_denda', 50000))
        konfig.maks_buku      = int(data.get('maks_buku', 3))
        konfig.save()

    def handle(self, request):
        cek = self._redirect_if_not_login(request)
        if cek:
            return cek

        konfig, _ = Konfigurasi.objects.get_or_create(pk=1)

        if request.method == 'POST':
            action_type = request.POST.get('action_type')
            try:
                if action_type == 'update_profile':
                    self.__update_profile(request)
                    messages.success(request, 'Profil admin berhasil diperbarui!')
                elif action_type == 'change_password':
                    self.__change_password(request)
                    messages.success(request, 'Kata sandi berhasil diubah!')
                elif action_type == 'update_circulation':
                    self.__update_circulation(konfig, request.POST)
                    messages.success(request, 'Aturan sirkulasi sistem berhasil disimpan!')
            except ValueError as e:
                messages.error(request, str(e), extra_tags='error')
            return redirect('settings') 

        return render(request, 'frontend/setting.html', {'konfig': konfig})