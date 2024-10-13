from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login

def custom_admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', '/admin/'))  # Ensure proper redirect

def trips_details(request):
    return render(request, 'trips_details.html')