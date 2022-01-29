from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm

def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        data = request.POST
        user = authenticate(username=data['login'], password=data['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/schedule/')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form })

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('/')