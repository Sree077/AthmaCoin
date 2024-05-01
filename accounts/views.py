from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

def register(request):
    if request.method == 'POST':
        full_name = request.POST['fname']
        phone_number = request.POST['Phno']
        email = request.POST['email']
        password1 = request.POST['pass1']

        if CustomUser.objects.filter(email=email).exists():
            messages.info(request, "Email already taken!")
            return redirect("register")
        else:
            user = CustomUser.objects.create_user(username=email, email=email, password=password1)
            user.phone_number = phone_number
            user.first_name = full_name.split()[0]  
            user.last_name = ' '.join(full_name.split()[1:])  
            user.save()

            user = authenticate(request, username=email, password=password1)
            if user is not None:
                auth_login(request, user)
                messages.success(request, "Registration successful! You are now logged in.")
                return redirect('profile')  
            else:
                messages.error(request, "User authentication failed after registration.")

    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('profile')  
        else:
            messages.error(request, "Invalid login credentials!")
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def profile(request):
    leaderboard = CustomUser.objects.order_by('-AthmaCoin').values_list('first_name', 'last_name', 'AthmaCoin')
    return render(request,"home.html",{"leaderboard": leaderboard})




def claim_athmacoin(request):
    pass