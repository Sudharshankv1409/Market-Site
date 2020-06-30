from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .decorators import should_not_be_logged_in
from django.utils.decorators import method_decorator
from .models import User
from secrets import token_urlsafe
from django.contrib.sites.shortcuts import get_current_site
from yuvraj_silk.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from .forms import ForgotPasswordForm

# Create your views here.

@method_decorator(should_not_be_logged_in,name = 'dispatch')
class LoginView(View):

    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        # remember_me = request.POST.get('selector')
        user = authenticate(username=email, password=password)
        if user:
            if user.is_verified:
                login(request, user)
                messages.success(request, 'Logged in successfully')
                return redirect(reverse('home'))
            else:
                messages.warning(request,'Email Not Verified')
                return redirect(reverse('users:login'))
        else:
            messages.warning(request, 'Incorrect Login Information')
        return redirect(reverse('users:login'))

class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        messages.success(request, 'Logged out successfully')
        return redirect(reverse('home'))

@method_decorator(should_not_be_logged_in, name='dispatch')
class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'users/forgotpassword.html')

    def post(self, request):
        email = request.POST.get('email')
        if not User.objects.filter(email=email).exists():
            messages.warning(request, 'User with Email Address does not exists')
            return redirect(reverse('users:forgot_password'))

        token = token_urlsafe(25)
        domain = get_current_site(request).domain
        changepassword_link = 'http://{}/users/changepassword?email={}&token={}'.format(domain, email, token)
        message = """
        		Hello there!
        		Here is the link to change your password.
        		Click Here: {}
                """.format(changepassword_link)
        try:
            send_mail('Change Password', message, 'Yuvraj Silk', [email], fail_silently=False, html_message=None)
            user = User.objects.get(email=email)
            user.token = token
            user.save()
            messages.success(request,"Password Change Link is sent! Please Check Your Email!")
            return redirect(reverse('users:login'))
        except Exception as e:
            print(e)
            messages.error(request,'Validation Error')
            return redirect(reverse('users:forgot_password'))

@method_decorator(should_not_be_logged_in,name = 'dispatch')
class RegisterView(View):
    def get(self, request):
        return render(request, 'users/register.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        lname = request.POST.get('lname')
        fname = request.POST.get('fname')
        phone = request.POST.get('phone')

        if User.objects.filter(email=email).exists():
            messages.warning(request, 'User with Email Address already exists')
            return redirect(reverse('users:register'))

        if User.objects.filter(phone_number=phone).exists():
            messages.warning(request, 'User with Phone Number already exists')
            return redirect(reverse('users:register'))

        if not password == cpassword:
            messages.warning(request, "Passwords don't match")
            return redirect(reverse('users:register'))

        if not (password and cpassword):
            messages.warning(request, "Passwords are required")
            return redirect(reverse('users:register'))

        token = token_urlsafe(25)
        domain = get_current_site(request).domain
        verification_url = 'http://{}/users/verify?email={}&token={}'.format(domain, email, token)
        message = """
        		Thank you for signing up!
        		Verify your Email using the link below.
        		Click Here: {}
                """.format(verification_url)

        try:
            send_mail('Signup Vertification', message, 'Yuvraj Silk', [email], fail_silently=False, html_message=None)
            user = User.objects.create_user(email=email, phone_number = phone, password=password)
            user.first_name = fname
            user.last_name = lname
            user.gender = gender
            user.dob = dob
            user.token = token
            user.save()
            messages.success(request,"Vertification Link Sent! Please Check Your Email!")
            return redirect(reverse('users:login'))
        except Exception as e:
            print(e)
            messages.error(request,'Registration Failed Please Check whether you have entered all the fields')
            return redirect(reverse('users:register'))

class EmailVerifyView(View):
    def get(self, request):
        email = request.GET.get('email')
        token = request.GET.get('token')
        user = User.objects.get(email=email)
        if not user:
            messages.error(request, 'Invalid User')
            return redirect(reverse('users:login'))
        if not user.token == token:
            messages.error(request, 'Invalid Token')
            return redirect(reverse('users:login'))
        user.is_verified = True
        user.token = None
        user.save()
        messages.success(request, 'Email Verified Please Login')
        return redirect(reverse('users:login'))

class ChangePasswordView(View):
    def get(self, request):
        email = request.GET.get('email')
        token = request.GET.get('token')
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            print(e,email)
            messages.error(request, 'Invalid User')
            return redirect(reverse('users:forgot_password'))
        if not user.token == token:
            messages.error(request, 'Invalid Token')
            return redirect(reverse('users:forgot_password'))
        return render(request, 'users/changepassword.html')

    def post(self, request):
        email = request.GET.get('email')
        token = request.GET.get('token')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'Invalid User')
            return redirect(reverse('users:forgot_password'))
        if not user.token == token:
            messages.error(request, 'Invalid Token')
            return redirect(reverse('users:forgot_password'))
        if not new_password == confirm_password:
            messages.warning(request, "Passwords don't match")
            domain = get_current_site(request).domain
            changepassword_link = 'http://{}/users/changepassword?email={}&token={}'.format(domain, email, token)
            return redirect(changepassword_link)

        user.set_password(new_password)
        user.token = None
        user.save()
        messages.success(request, 'Password Changed Successfully')
        return redirect(reverse('users:login'))
