from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from .models import *
from .models import Profile

# Create your views here.
def home(request):
    return render(request, 'index.html')

def RegisterView(request):
    if request.method == "POST":
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request, f'{username} already token. Please try another one.')
            return redirect('/register/')
        
        user = User.objects.filter(email=email)
        if user.exists():
            messages.info(request, f'{email} already token. Please try another one.')
            return redirect('/register/')
        
        if password1 != password2:
            messages.error(request, "Password Doesn't match.")
            return redirect('/register/')
        elif len(password1) < 5:
            messages.error(request, "Password should be at least 5 characters.")
            return redirect('/register/')
        
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,        
        )
        user.set_password(password2)
        user.save()
        messages.success(request, f'{username}! Your accounts create successfully.')
        return redirect('/login/')
    return render(request, '../templates/auth/register.html')

def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            messages.success(request, f'{username} ! You have successfully logged in.')
            login(request, user)
            if not user.is_superuser:  # Only check profiles for non-admin users
                try:
                    profile = user.profile
                except Profile.DoesNotExist:
                    # Create a profile if it's missing
                    Profile.objects.create(user=user)
            if not remember_me:
                request.session.set_expiry(0)
                request.session.modified = True
            else:
                request.session.set_expiry(1209600)
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            return redirect('profile', username=user.username)
        else:
            if not User.objects.filter(username=username).exists():
                messages.error(request, f'{username}! Invalid username.')
            else:
                messages.error(request, f'Invalid password.')
                return redirect('/login/')
    
    return render(request, '../templates/auth/login.html')


def LogoutView(request):
    logout(request)
    messages.success(request,  'You have successfully logged out.')
    return redirect('/login/')

class PasswordChangeView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'auth/password-change/change_password.html'
    success_url = reverse_lazy("password_change_done")
    
    def post(self, request, *args, **kwargs):
        
        old_password: str = request.POST.get('old_password')
        new_password1: str = request.POST.get('new_password1')
        new_password2: str = request.POST.get('new_password2')
        
        user = request.user
        
        if not user.check_password(old_password):
            messages.warning(request, "Old Password doesn't match. Please Try Again!")
            return redirect('password_change')
        
        if len(new_password1)< 8:
            messages.warning(request, "Password must be at least 8 characters long")
            return redirect('password_change')
        
        if old_password == new_password1:
            messages.warning(request, "New Password can't be same as Old Password")
            return redirect('password_change')
        
        if new_password1 != new_password2:
            messages.warning(request, "New Passwords doesn't match. Please Try Again!")
            return redirect('password_change')
        
        user.set_password(new_password1)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Your password has been changed successfully. new password would take effect on next login.")
        return redirect('password_change_done')
    
 
class PasswordResetView(LoginRequiredMixin, auth_views.PasswordResetView):
    template_name = 'auth/password-reset/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        if email != request.user.email:
            messages.error(request,  "You can only reset your password using your registered email address.")
            return redirect('password_reset')
        
        return super().post(request, *args, **kwargs)




class PasswordResetConfirmView(LoginRequiredMixin, auth_views.PasswordResetConfirmView):
    template_name = 'auth/password-reset/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in first to reset your password.")
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = "Please enter your new password below."  
        context['username'] = self.request.user.username
        return context

    def post(self, request, *args, **kwargs):
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        # Check if the new passwords match
        if new_password1 != new_password2:
            messages.warning(request, "New passwords do not match. Please try again!")
            return render(request, self.template_name, self.get_context_data(**kwargs))

        # Check if the user is authorized to reset the password
        user = self.get_user(kwargs.get('uidb64'))  # Get user by uidb64
        if user and user.email != request.user.email:
            messages.error(request, "You can only reset your password using your registered email address.")
            return redirect('password_reset')

        # Set the new password
        request.user.set_password(new_password1)
        request.user.save()
        messages.success(request, "Your password has been reset successfully!")
        return redirect(self.success_url)


    def get_user(self, uidb64):
        from django.utils.http import urlsafe_base64_decode
        from django.contrib.auth.models import User
        from django.contrib.auth.tokens import default_token_generator

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            return User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None

    
 





@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)  
    profile = get_object_or_404(Profile, user=user)    
    context = {
        'user': user,
        'profile': profile,
    }
    if request.user.is_authenticated and not request.user.is_superuser:
        try:
            # Try to access the user's profile
            profile = request.user.profile
        except Profile.DoesNotExist:
            # Handle the missing profile for non-admin users
            Profile.objects.create(user=request.user)
    return render(request, 'auth/profile.html', context)


# robots.txt
from django.shortcuts import HttpResponse
from django.views.decorators.http import require_GET
@require_GET
def robots_txt(request):
    content = "User-agent: *\nDisallow: /"
    return HttpResponse(content, content_type="text/plain")