from django.shortcuts import render
from django.db.models import Count
import json
from ..models import Buku, Anggota, Pinjaman
from .base import BaseView
from datetime import date, timedelta

class DashboardView(BaseView):
    def __get_statistik(self):
        for p in Pinjaman.objects.filter(status__in=['dipinjam', 'terlambat']):
            p.perbarui_status()

        query_tren = Pinjaman.objects.values('tanggal_pinjam') \
                                     .annotate(total=Count('id')) \
                                     .order_by('tanggal_pinjam')

        labels = []
        data_tren = []
        
        for item in query_tren:
            if item['tanggal_pinjam']:
                tgl_format = item['tanggal_pinjam'].strftime('%d/%m')
                labels.append(tgl_format)
                data_tren.append(item['total'])
        
        total_peminjaman = sum(data_tren)
        total_hari_aktif = len(data_tren) if len(data_tren) > 0 else 1
        rata_rata = round(total_peminjaman / total_hari_aktif, 1)

        max_tren = max(data_tren) if data_tren else 0
        mid_tren = int(max_tren / 2) if max_tren > 1 else ""

        return {
            'total_buku'    : Buku.objects.count(),
            'total_anggota' : Anggota.objects.count(),
            'dipinjam'      : Pinjaman.objects.filter(status='dipinjam').count(),
            'terlambat'     : Pinjaman.objects.filter(status='terlambat').count(),
            'aktivitas'     : Pinjaman.objects.select_related('buku', 'anggota').order_by('-id')[:5],
            
            'tren_labels'     : json.dumps(labels),      
            'tren_peminjaman' : json.dumps(data_tren),   
            'rata_rata_pinjam': rata_rata,

            'max_tren' : max_tren,
            'mid_tren' : mid_tren,
        }

    def handle(self, request):
        cek = self._redirect_if_not_login(request)
        if cek:
            return cek
        return render(request, 'frontend/tampilan_dashboard.html', self.__get_statistik())