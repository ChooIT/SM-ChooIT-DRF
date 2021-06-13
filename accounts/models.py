import pytz
from django.conf import settings
from django.db import models
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.urls import reverse
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, type, password=None, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, type=type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, type, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, type, password, **extra_fields)

    def create_superuser(self, email, type, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, type, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    customized User
    """

    email = models.EmailField(
        verbose_name=_("email id"), max_length=64, unique=True, help_text="EMAIL ID."
    )
    type = models.CharField(
        _("user type"),
        max_length=1,
        choices=(
            ("i", "individual"),
            ("b", "business"),
            ("a", "ADMIN"),
        ),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    active_level = models.IntegerField(default=0)
    gender = models.CharField(
        _("gender type"),
        max_length=1,
        choices=(
            ('w', 'woman'),
            ('m', 'man'),
            ('n', 'null')
        )
    )
    nickname = models.CharField(max_length=35)
    emoji = models.CharField(max_length=3)
    created_at = models.DateTimeField(_("date joined"), auto_now_add=True)
    updated_at = models.DateTimeField(_("date_updated"), auto_now=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["type"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.email

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     """
    #     Send an email to this User.
    #     """
    #     send_mail(subject, message, from_email, [self.email], **kwargs)


class Nickname(models.Model):
    part = models.CharField(
        _("품사"),
        max_length=1,
        choices=(
            ("a", "형용사"),
            ("n", "명사")
        ),
        default="a"
    )
    content = models.CharField(max_length=10, null=True)
    emoji = models.CharField(max_length=3, null=True)

    class Meta:
        ordering = ['part']


class NicknameArchive(models.Model):
    nickname = models.CharField(max_length=30)
    count = models.IntegerField(default=1)

    def __str__(self):
        return "%s%d" % (self.nickname, self.count)


class Tag(models.Model):
    tag_text = models.CharField(max_length=10, null=False)
    tag_code = models.AutoField(primary_key=True)

    def __str__(self):
        return "[%d] %s" % (self.tag_code, self.tag_text)

    class Meta:
        ordering = ['tag_code']


class UserTag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
