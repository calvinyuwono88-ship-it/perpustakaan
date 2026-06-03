from .models import Pinjaman

def global_header_context(request):
    if request.user.is_authenticated:
        
        total_terlambat = Pinjaman.objects.filter(status='terlambat').count()
        
        full_name = request.user.get_full_name() or request.user.username

        initials = "".join([name[0].upper() for name in full_name.split()[:2]])
        
        return {
            'global_notif_count': total_terlambat,
            'global_user_initials': initials or "AD"
        }
    return {
        'global_notif_count': 0,
        'global_user_initials': "??"
    }