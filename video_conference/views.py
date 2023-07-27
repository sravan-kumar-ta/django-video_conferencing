from decouple import config
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from video_conference.forms import RegisterForm, LoginForm


def home(request):
    return render(request, 'dashboard.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please login.")
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': RegisterForm})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')

        messages.error(request, "Invalid credentials. Please try again.")
        return render(request, 'login.html', {'form': form})

    return render(request, 'login.html', {'form': LoginForm()})


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def video_call(request):
    context = {
        'name': request.user.first_name + " " + request.user.last_name,
        'appID': config('ZEGOCLOUD_ID'),
        'serverSecret': config('SERVER_SECRET'),
    }
    return render(request, 'video_call.html', context=context)


@login_required
def join_room(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/meeting?roomID=" + roomID)
    return render(request, 'join_room.html')
