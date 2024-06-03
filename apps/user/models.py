from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from .tasks import send


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if email is None:
            raise TypeError("Users must have an email address.")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ABITURIENT = 'ABITURIENT', _('ABITURIENT')
        DEAN = 'DEAN', 'Dean'
        COMMISSIONER = 'COMMISSIONER', 'Commissioner'
        ASSISTANT = 'ASSISTANT', 'Assistant'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.DEAN)
    department = models.ForeignKey('abiturient.Department', on_delete=models.CASCADE, related_name='users', blank=True,
                                   null=True)

    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="First Name")
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Last Name")
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ("-id",)
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email


class Invitation(models.Model):
    class RoleChoices(models.TextChoices):
        ABITURIENT = 'ABITURIENT', _('ABITURIENT')
        DEAN = 'DEAN', 'Dean'
        COMMISSIONER = 'COMMISSIONER', 'Commissioner'
        ASSISTANT = 'ASSISTANT', 'Assistant'

    role = models.CharField(max_length=255, choices=RoleChoices.choices, default=RoleChoices.DEAN)
    department = models.ForeignKey('abiturient.Department', on_delete=models.CASCADE, related_name='invitations')
    invitation_token = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.pk:
            subject = "Invitation to join our platform"
            invitation_token = str(uuid.uuid4())
            self.invitation_token = invitation_token

            send(subject=subject, email=self.email, token=invitation_token)
        super().save(*args, **kwargs)
