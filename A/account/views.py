from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views import View
from . forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from . models import Relations
from django.contrib import messages
# Create your views here.



class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request,'you are registered and cant register again now')
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name , {'form': form})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            messages.success(request, 'you rtegistered successfully', 'success')
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})
        

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request,'you are logged in and cant login again now')
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)
        

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name , {'form': form})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username = cd['username'], password = cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'logged in successfully', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'invalid username or password', 'warning')
        return render(request, self.template_name, {'form': form})



class UserLogoutView(LoginRequiredMixin, View):
    login_url = '/account/login/'


    def get(self, request):
        logout(request)
        messages.success(request, ' you logged out', 'success')
        return redirect('home:home')



class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        is_following = False
        user = get_object_or_404(User, id = user_id)
        posts = user.posts.all()
        relation = Relations.objects.filter(from_user = request.user, to_user = user)
        if relation.exists():
            is_following = True
        return render(request, 'account/profile.html', {'user': user, 'posts': posts, 'is_following': is_following})
    








class UserPasswordResetView(PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'
    
class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')

class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'



class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id = user_id) # the person who i want to follow
        relation = Relations.objects.filter(from_user = request.user, to_user = user)
        if relation.exists():
            messages.error(request,'you are already following this user', 'danger')
        else:
            Relations.objects.create(from_user = request.user, to_user = user)
            messages.success(request, 'you are now following this user', 'success')
        return redirect('account:user_profile', user.id)
            



class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id = user_id)
        relation = Relations.objects.filter(from_user = request.user, to_user = user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'you are no longer following this user', 'success')
        else:
            messages.error('you are not following this user', 'danger')
        return redirect('account:user_profile', user.id)
    



