from django.shortcuts import redirect

class BaseView:
    """
    Kelas dasar abstrak untuk semua view.
    Menerapkan Abstraksi dan Enkapsulasi.
    """
    def handle(self, request, *args, **kwargs):
        raise NotImplementedError("Subclass harus implementasi handle()")

    def _redirect_if_not_login(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        return None