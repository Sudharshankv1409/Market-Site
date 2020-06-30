from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_delete,post_save,pre_save

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        if not phone_number:
            raise ValueError('Users must have the phone number')

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password):
        user = self.create_user(
                email = self.normalize_email(email),
                password = password,
                phone_number = phone_number,
        )
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.is_verified = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    date_of_birth = models.DateTimeField(verbose_name='date of birth', blank=True, null=True)
    gender = models.CharField(max_length=6, choices=(('male','Male'),('female','Female')), blank=True, null=True)
    profile_pic = models.ImageField(upload_to="users/profile_pics/", blank = True)
    token = models.CharField(max_length=30, blank=True, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number',]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"
        return None

    def get_short_name(self):
        if self.first_name:
            return self.first_name.capitalize()
        return None

    def has_perm(self, obj=None):
        return True

    def has_module_perms(self,app_label):
        return True
