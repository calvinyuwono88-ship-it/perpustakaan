from django.shortcuts import redirect
from django.contrib.auth import logout

# Impor semua fungsionalitas dari file terpisah
from .authentikasi import LoginView
from .dashboard import DashboardView
from .manajemenbuku import BukuView
from .anggota import AnggotaView
from .pinjaman import PinjamanView
from .settings import SettingsView

# Instansiasi objek view Singleton-like pattern untuk penanganan request
_dashboard     = DashboardView()
_buku_view     = BukuView()
_anggota_view  = AnggotaView()
_pinjaman_view = PinjamanView()
_settings_view = SettingsView()

# Fungsi pembungkus URL wrapper functions yang dibaca oleh urls.py
def login_view(request):         return LoginView(request)        
def logout_view(request):        logout(request); return redirect('login')
def dashboard(request):          return _dashboard.handle(request)
def kelola_buku(request):        return _buku_view.handle(request)
def edit_buku(request, pk):      return _buku_view.handle_edit(request, pk)
def hapus_buku(request, pk):     return _buku_view.handle(request, pk=pk)
def kelola_anggota(request):     return _anggota_view.handle(request)
def hapus_anggota(request, pk):  return _anggota_view.handle(request, pk=pk)
def catatan_pinjaman(request):   return _pinjaman_view.handle(request)
def kembalikan_buku(request, pk):return _pinjaman_view.handle(request, pk=pk)
def hapus_pinjaman(request, pk): return _pinjaman_view.handle(request, pk=pk)
def settings_view(request):      return _settings_view.handle(request)