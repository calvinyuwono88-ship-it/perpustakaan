from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def LoginView(request):
    if request.method == 'POST':
        username_kamu = request.POST.get('username')
        password_kamu = request.POST.get('password')
        user = authenticate(request, username=username_kamu, password=password_kamu)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard') 
        else:
            return render(request, 'frontend/menulogin.html', {'error': 'Username atau Password salah!'})
            
    return render(request, 'frontend/menulogin.html')