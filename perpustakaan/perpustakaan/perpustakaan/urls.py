from django.urls import path
from . import views

urlpatterns = [
    path('',                         views.login_view,        name='login'),
    path('login/',                    views.login_view,        name='login'),
    path('logout/',                   views.logout_view,       name='logout'),
    path('dashboard/',                views.dashboard,         name='dashboard'),
    path('books/',                    views.kelola_buku,       name='kelola_buku'),
    path('books/delete/<int:pk>/',    views.hapus_buku,        name='hapus_buku'),
    path('books/edit/<int:pk>/',      views.edit_buku,         name='edit_buku'),
    
    
    # KELOLA ANGGOTA
    path('members/',                  views.kelola_anggota,    name='kelola_anggota'),
    path('members/delete/<int:pk>/',  views.hapus_anggota,     name='hapus_anggota'), 
    
    # PINJAMAN & SETTING
    path('loans/',                    views.catatan_pinjaman,  name='catatan_pinjaman'),
    path('loans/return/<int:pk>/',    views.kembalikan_buku,   name='kembalikan_buku'),
    path('settings/',                 views.settings_view,     name='settings'),
    path('loans/delete/<int:pk>/', views.hapus_pinjaman, name='hapus_pinjaman'),

    
]